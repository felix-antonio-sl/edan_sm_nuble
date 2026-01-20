/**
 * EDAN Salud Mental - JavaScript del Wizard
 * Funcionalidades interactivas
 */

document.addEventListener('DOMContentLoaded', function() {
    // Formateo automático del RUN
    const runInput = document.getElementById('run');
    if (runInput) {
        runInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/[^\dkK]/g, '');
            
            if (value.length > 9) {
                value = value.slice(0, 9);
            }
            
            // Formatear con puntos y guión
            if (value.length > 1) {
                let formatted = '';
                const body = value.slice(0, -1);
                const dv = value.slice(-1).toUpperCase();
                
                // Agregar puntos
                const reversed = body.split('').reverse();
                for (let i = 0; i < reversed.length; i++) {
                    if (i > 0 && i % 3 === 0) {
                        formatted = '.' + formatted;
                    }
                    formatted = reversed[i] + formatted;
                }
                
                if (body.length > 0) {
                    formatted += '-' + dv;
                }
                
                e.target.value = formatted;
            }
        });
    }

    // Auto-guardar el paso actual (visual feedback)
    const wizardForm = document.querySelector('.wizard-form');
    if (wizardForm) {
        const inputs = wizardForm.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                // Agregar indicador visual de cambio guardado
                this.classList.add('input-saved');
                setTimeout(() => {
                    this.classList.remove('input-saved');
                }, 1000);
            });
        });
    }

    // Validación de campos requeridos antes de enviar
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('input-error');
                    isValid = false;
                } else {
                    field.classList.remove('input-error');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                // Scroll al primer campo con error
                const firstError = form.querySelector('.input-error');
                if (firstError) {
                    firstError.focus();
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    });

    // Animación de botones al hacer clic
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', function() {
            this.classList.add('btn-clicked');
            setTimeout(() => {
                this.classList.remove('btn-clicked');
            }, 200);
        });
    });

    // Highlight de filas al seleccionar opción
    const radioLabels = document.querySelectorAll('.radio-label');
    radioLabels.forEach(label => {
        label.addEventListener('click', function() {
            const row = this.closest('.factors-row');
            if (row) {
                row.classList.add('row-selected');
                setTimeout(() => {
                    row.classList.remove('row-selected');
                }, 300);
            }
        });
    });

    // Contador de caracteres para textareas
    const textareas = document.querySelectorAll('.form-textarea');
    textareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        if (maxLength) {
            const counter = document.createElement('span');
            counter.className = 'char-counter';
            counter.textContent = `0/${maxLength}`;
            textarea.parentNode.appendChild(counter);
            
            textarea.addEventListener('input', function() {
                counter.textContent = `${this.value.length}/${maxLength}`;
                if (this.value.length > maxLength * 0.9) {
                    counter.classList.add('char-warning');
                } else {
                    counter.classList.remove('char-warning');
                }
            });
        }
    });

    // Smooth scroll para barra de progreso
    const progressSteps = document.querySelectorAll('.progress-step');
    progressSteps.forEach(step => {
        step.addEventListener('click', function() {
            const wizardContent = document.querySelector('.wizard-content');
            if (wizardContent) {
                wizardContent.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});

// Estilos dinámicos para validación
const style = document.createElement('style');
style.textContent = `
    .input-error {
        border-color: var(--danger) !important;
        animation: shake 0.5s ease;
    }
    
    .input-saved {
        border-color: var(--success) !important;
        background-color: var(--success-light) !important;
    }
    
    .btn-clicked {
        transform: scale(0.95);
    }
    
    .row-selected {
        background-color: var(--info-light) !important;
    }
    
    .char-counter {
        display: block;
        text-align: right;
        font-size: var(--font-size-xs);
        color: var(--gray-400);
        margin-top: var(--spacing-xs);
    }
    
    .char-warning {
        color: var(--warning);
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        20%, 60% { transform: translateX(-5px); }
        40%, 80% { transform: translateX(5px); }
    }
`;
document.head.appendChild(style);
