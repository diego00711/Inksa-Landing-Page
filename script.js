// URLs de redirecionamento por perfil
// No futuro, substitua pelos links da Play Store correspondentes
const URL_CLIENTE      = 'https://clientes.inksadelivery.com.br';
const URL_RESTAURANTE  = 'https://restaurante.inksadelivery.com.br';
const URL_ENTREGADOR   = 'https://entregadores.inksadelivery.com.br';

const PERFIL_URLS = {
    cliente:     URL_CLIENTE,
    restaurante: URL_RESTAURANTE,
    entregador:  URL_ENTREGADOR,
};

document.addEventListener('DOMContentLoaded', () => {
    const customSelect  = document.querySelector('.custom-select-wrapper');
    const selectSelected = customSelect.querySelector('.select-selected');
    const selectItems   = customSelect.querySelector('.select-items');
    const options       = selectItems.querySelectorAll('div');
    const confirmBtn    = document.getElementById('btn-confirmar');

    let selectedValue = null;

    selectSelected.addEventListener('click', (e) => {
        e.stopPropagation();
        selectItems.classList.toggle('select-hide');
        selectSelected.classList.toggle('select-arrow-active');
    });

    options.forEach(option => {
        option.addEventListener('click', function () {
            selectedValue = this.getAttribute('data-value');
            selectSelected.innerHTML = this.textContent + ' <i class="fas fa-chevron-down arrow"></i>';
            selectItems.classList.add('select-hide');
            selectSelected.classList.remove('select-arrow-active');

            options.forEach(o => o.classList.remove('selected'));
            this.classList.add('selected');
        });
    });

    confirmBtn.addEventListener('click', () => {
        if (!selectedValue) {
            alert('Por favor, selecione seu perfil antes de continuar.');
            return;
        }
        const url = PERFIL_URLS[selectedValue];
        if (url) {
            window.location.href = url;
        }
    });

    document.addEventListener('click', (event) => {
        if (!customSelect.contains(event.target)) {
            selectItems.classList.add('select-hide');
            selectSelected.classList.remove('select-arrow-active');
        }
    });
});
