#include <stdint.h>
#define STM32F411xE
#include "stm32f4xx.h"
#include <string.h>

// System States
typedef enum {
    STATE_IDLE,
    STATE_TOOLS,
    STATE_SETTINGS,
    STATE_WIFI_TEST,
    STATE_THRESHOLD,
    STATE_CALIBRATION,
    STATE_MONITOR,
    STATE_ALERT,
    STATE_SNOOZE
} SystemState_t;

// Global Variables
SystemState_t current_state = STATE_IDLE;
uint32_t moisture_value = 0;
uint32_t temperature_value = 0;
uint32_t light_value = 0;
uint32_t threshold_low = 1000;
uint32_t threshold_high = 3000;
uint32_t hysteresis = 100;
uint8_t alert_active = 0;
uint32_t snooze_timer = 0;
uint32_t system_tick = 0;

// Function Prototypes
void System_Init(void);
void GPIO_Init(void);
void ADC_Init(void);
void Timer_Init(void);
void Read_Sensors(void);
void Process_State_Machine(void);
void Handle_Button_Press(uint8_t button);
void OLED_Display_Update(void);
void Alert_Handler(void);

// Button interrupt handler
void EXTI4_IRQHandler(void) {
    if ((EXTI->PR & EXTI_PR_PR4) != 0) {
        if ((GPIOB->IDR & GPIO_IDR_IDR_4) == 0) {
            // Button pressed - BTN1 (Enter/Tools)
            Handle_Button_Press(1);
        }
        EXTI->PR |= EXTI_PR_PR4;
    }
}

void EXTI9_5_IRQHandler(void) {
    if ((EXTI->PR & EXTI_PR_PR5) != 0) {
        if ((GPIOB->IDR & GPIO_IDR_IDR_5) == 0) {
            // Button pressed - BTN2 (Settings/Back)
            Handle_Button_Press(2);
        }
        EXTI->PR |= EXTI_PR_PR5;
    }
    
    if ((EXTI->PR & EXTI_PR_PR6) != 0) {
        if ((GPIOB->IDR & GPIO_IDR_IDR_6) == 0) {
            // Button pressed - BTN3 (Ack/Snooze)
            Handle_Button_Press(3);
        }
        EXTI->PR |= EXTI_PR_PR6;
    }
}

// System timer interrupt (1ms)
void TIM2_IRQHandler(void) {
    if (TIM2->SR & TIM_SR_UIF) {
        system_tick++;
        
        // Snooze timer countdown
        if (snooze_timer > 0) {
            snooze_timer--;
        }
        
        TIM2->SR &= ~TIM_SR_UIF;
    }
}

void System_Init(void) {
    // Enable clocks
    RCC->AHB1ENR |= (RCC_AHB1ENR_GPIOAEN | RCC_AHB1ENR_GPIOBEN | RCC_AHB1ENR_GPIOCEN);
    RCC->APB1ENR |= RCC_APB1ENR_TIM2EN;
    RCC->APB2ENR |= (RCC_APB2ENR_SYSCFGEN | RCC_APB2ENR_ADC1EN);
    
    GPIO_Init();
    ADC_Init();
    Timer_Init();
    
    current_state = STATE_IDLE;
}

void GPIO_Init(void) {
    // LED PA5 setup
    GPIOA->MODER &= ~GPIO_MODER_MODER5;
    GPIOA->MODER |= (0b01 << GPIO_MODER_MODER5_Pos);
    GPIOA->OTYPER &= ~GPIO_OTYPER_OT5;
    GPIOA->OSPEEDR &= ~GPIO_OSPEEDER_OSPEEDR5;
    
    // Buttons setup (PB4, PB5, PB6)
    GPIOB->MODER &= ~(GPIO_MODER_MODER4 | GPIO_MODER_MODER5 | GPIO_MODER_MODER6);
    GPIOB->PUPDR &= ~(GPIO_PUPDR_PUPDR4 | GPIO_PUPDR_PUPDR5 | GPIO_PUPDR_PUPDR6);
    GPIOB->PUPDR |= (0b01 << GPIO_PUPDR_PUPD4_Pos) | 
                    (0b01 << GPIO_PUPDR_PUPD5_Pos) | 
                    (0b01 << GPIO_PUPDR_PUPD6_Pos);
    
    // Sensor inputs (PC0 - moisture, PC1 - temperature, PC2 - light)
    GPIOC->MODER |= (0b11 << GPIO_MODER_MODER0_Pos) |
                    (0b11 << GPIO_MODER_MODER1_Pos) |
                    (0b11 << GPIO_MODER_MODER2_Pos);
    
    // EXTI setup for buttons
    EXTI->IMR |= EXTI_IMR_IM4 | EXTI_IMR_IM5 | EXTI_IMR_IM6;
    EXTI->FTSR |= EXTI_FTSR_TR4 | EXTI_FTSR_TR5 | EXTI_FTSR_TR6;
    
    SYSCFG->EXTICR[1] &= ~(SYSCFG_EXTICR2_EXTI4 | SYSCFG_EXTICR2_EXTI5 | SYSCFG_EXTICR2_EXTI6);
    SYSCFG->EXTICR[1] |= (0b01 << SYSCFG_EXTICR2_EXTI4_Pos) |
                         (0b01 << SYSCFG_EXTICR2_EXTI5_Pos) |
                         (0b01 << SYSCFG_EXTICR2_EXTI6_Pos);
    
    NVIC_EnableIRQ(EXTI4_IRQn);
    NVIC_EnableIRQ(EXTI9_5_IRQn);
}

void ADC_Init(void) {
    // ADC1 configuration
    ADC1->CR2 |= ADC_CR2_ADON;
    ADC1->SMPR2 |= (0b111 << ADC_SMPR2_SMP0_Pos) |
                   (0b111 << ADC_SMPR2_SMP1_Pos) |
                   (0b111 << ADC_SMPR2_SMP2_Pos);
}

void Timer_Init(void) {
    // Timer 2 for 1ms interrupt
    TIM2->PSC = 8400 - 1;  // Prescaler for 10kHz
    TIM2->ARR = 10 - 1;    // Auto reload for 1ms
    TIM2->DIER |= TIM_DIER_UIE;
    TIM2->CR1 |= TIM_CR1_CEN;
    
    NVIC_EnableIRQ(TIM2_IRQn);
}

void Read_Sensors(void) {
    // Read moisture sensor (PC0/ADC1_IN10)
    ADC1->SQR3 = 10;
    ADC1->CR2 |= ADC_CR2_SWSTART;
    while (!(ADC1->SR & ADC_SR_EOC));
    moisture_value = ADC1->DR;
    
    // Read temperature sensor (PC1/ADC1_IN11)
    ADC1->SQR3 = 11;
    ADC1->CR2 |= ADC_CR2_SWSTART;
    while (!(ADC1->SR & ADC_SR_EOC));
    temperature_value = ADC1->DR;
    
    // Read light sensor (PC2/ADC1_IN12)
    ADC1->SQR3 = 12;
    ADC1->CR2 |= ADC_CR2_SWSTART;
    while (!(ADC1->SR & ADC_SR_EOC));
    light_value = ADC1->DR;
}

void Handle_Button_Press(uint8_t button) {
    switch (current_state) {
        case STATE_IDLE:
            if (button == 1) {
                current_state = STATE_TOOLS;
            } else if (button == 2) {
                current_state = STATE_SETTINGS;
            }
            break;
            
        case STATE_TOOLS:
            if (button == 1) {
                current_state = STATE_WIFI_TEST;
            } else if (button == 2) {
                current_state = STATE_IDLE;
            }
            break;
            
        case STATE_SETTINGS:
            if (button == 1) {
                current_state = STATE_THRESHOLD;
            } else if (button == 2) {
                current_state = STATE_IDLE;
            }
            break;
            
        case STATE_THRESHOLD:
            if (button == 1) {
                current_state = STATE_CALIBRATION;
            } else if (button == 2) {
                current_state = STATE_SETTINGS;
            }
            break;
            
        case STATE_CALIBRATION:
            if (button == 2) {
                current_state = STATE_MONITOR;
            }
            break;
            
        case STATE_MONITOR:
            if (button == 2) {
                current_state = STATE_IDLE;
            }
            break;
            
        case STATE_ALERT:
            if (button == 3) {
                current_state = STATE_SNOOZE;
                snooze_timer = 600000; // 10 minutes in ms
                alert_active = 0;
                GPIOA->ODR &= ~GPIO_ODR_OD5; // Turn off alert LED
            } else if (button == 2) {
                current_state = STATE_MONITOR;
                alert_active = 0;
                GPIOA->ODR &= ~GPIO_ODR_OD5;
            }
            break;
            
        case STATE_SNOOZE:
            if (snooze_timer == 0) {
                current_state = STATE_MONITOR;
            }
            break;
    }
}

void Process_State_Machine(void) {
    static uint32_t last_monitor_time = 0;
    
    switch (current_state) {
        case STATE_IDLE:
            // Display home screen
            break;
            
        case STATE_WIFI_TEST:
            // Perform WiFi connectivity test
            // Return to TOOLS after test
            current_state = STATE_TOOLS;
            break;
            
        case STATE_THRESHOLD:
            // Allow threshold adjustment
            break;
            
        case STATE_CALIBRATION:
            // Perform sensor calibration
            break;
            
        case STATE_MONITOR:
            // Read sensors every 1 second
            if (system_tick - last_monitor_time >= 1000) {
                Read_Sensors();
                last_monitor_time = system_tick;
                
                // Check thresholds
                if (moisture_value < threshold_low) {
                    current_state = STATE_ALERT;
                    alert_active = 1;
                }
            }
            break;
            
        case STATE_ALERT:
            Alert_Handler();
            break;
            
        case STATE_SNOOZE:
            if (snooze_timer == 0) {
                // Re-evaluate moisture after snooze
                Read_Sensors();
                if (moisture_value < threshold_low) {
                    current_state = STATE_ALERT;
                    alert_active = 1;
                } else {
                    current_state = STATE_MONITOR;
                }
            }
            break;
    }
}

void Alert_Handler(void) {
    static uint32_t blink_timer = 0;
    
    // Blink LED for attention
    if (system_tick - blink_timer >= 500) {
        GPIOA->ODR ^= GPIO_ODR_OD5;
        blink_timer = system_tick;
    }
}

void OLED_Display_Update(void) {
    // Update OLED display based on current state
    // This would interface with I2C OLED display
    switch (current_state) {
        case STATE_IDLE:
            // Show main menu
            break;
        case STATE_MONITOR:
            // Show sensor readings
            break;
        case STATE_ALERT:
            // Show alert message
            break;
        // Add other states as needed
    }
}

int main(void) {
    System_Init();
    
    while(1) {
        Process_State_Machine();
        OLED_Display_Update();
        
        // Small delay
        for (volatile int i = 0; i < 10000; i++);
    }
}