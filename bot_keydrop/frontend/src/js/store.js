const PRODUCTS = [
    { id: 'telegram_month', name: 'Integração Telegram', price: 'R$ 10,00/mês' },
    { id: 'premium_month', name: 'Assinatura Premium Mensal', price: 'R$ 49,99/mês' },
    { id: 'premium_year', name: 'Assinatura Premium Anual', price: 'R$ 539,90/ano (10% OFF)' },
    { id: 'frame_neon', name: 'Moldura Neon', price: 'R$ 7,99', frameClass: 'frame-neon' },
    { id: 'frame_diamond', name: 'Moldura Diamante', price: 'R$ 9,99', frameClass: 'frame-diamond' },
    { id: 'frame_gold', name: 'Moldura Dourada', price: 'R$ 5,99', frameClass: 'frame-gold' },
];

function renderProducts() {
    const container = document.getElementById('products');
    PRODUCTS.forEach(p => {
        const card = document.createElement('div');
        card.className = 'product-card';
        const highlight = p.id.includes('premium') ? ' <strong>★</strong>' : '';
        const preview = p.frameClass ?
            `<div class="avatar-preview ${p.frameClass}">👤</div>` : '';
        card.innerHTML = `${preview}<h3>${p.name}${highlight}</h3><p>${p.price}</p>`;
        container.appendChild(card);
    });
}

document.addEventListener('DOMContentLoaded', renderProducts);
