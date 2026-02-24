const API_BASE = '/api';

let allTerms = [];
let currentView = 'glossary';
let network = null;
let nodes = null;
let edges = null;

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    initializeNavigation();
    initializeGlossary();
    initializeGraph();
    initializeModals();
    loadTerms();
});

// Навигация
function initializeNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const view = btn.dataset.view;
            switchView(view);
        });
    });
}

function switchView(view) {
    currentView = view;
    
    // Обновить активные кнопки
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.view === view);
    });
    
    // Показать/скрыть представления
    document.querySelectorAll('.view').forEach(v => {
        v.classList.toggle('active', v.id === `${view}-view`);
    });
    
    if (view === 'graph') {
        loadGraph();
    }
}

// Глоссарий
function initializeGlossary() {
    const searchInput = document.getElementById('search-input');
    const categoryFilter = document.getElementById('category-filter');
    const addBtn = document.getElementById('add-term-btn');
    
    searchInput.addEventListener('input', filterTerms);
    categoryFilter.addEventListener('change', filterTerms);
    addBtn.addEventListener('click', () => openTermModal());
}

async function loadTerms() {
    try {
        const response = await fetch(`${API_BASE}/terms`);
        allTerms = await response.json();
        renderTerms(allTerms);
        updateCategoryFilter();
    } catch (error) {
        console.error('Ошибка загрузки терминов:', error);
        alert('Ошибка загрузки терминов');
    }
}

function renderTerms(terms) {
    const container = document.getElementById('terms-list');
    
    if (terms.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #999; padding: 40px;">Термины не найдены</p>';
        return;
    }
    
    container.innerHTML = terms.map(term => `
        <div class="term-card" data-keyword="${term.keyword}">
            <div class="term-card-header">
                <div>
                    <div class="term-title">${escapeHtml(term.title)}</div>
                    <div class="term-keyword">${escapeHtml(term.keyword)}</div>
                </div>
                ${term.category ? `<span class="term-category">${escapeHtml(term.category)}</span>` : ''}
            </div>
            <div class="term-definition">${escapeHtml(getTermDefinition(term.keyword))}</div>
            <div class="term-actions">
                <button class="btn-edit" onclick="event.stopPropagation(); editTerm('${term.keyword}')">Редактировать</button>
                <button class="btn-delete" onclick="event.stopPropagation(); deleteTerm('${term.keyword}')">Удалить</button>
            </div>
        </div>
    `).join('');
    
    // Добавить обработчики клика на карточки
    container.querySelectorAll('.term-card').forEach(card => {
        card.addEventListener('click', (e) => {
            if (!e.target.closest('.term-actions')) {
                const keyword = card.dataset.keyword;
                viewTerm(keyword);
            }
        });
    });
}

function getTermDefinition(keyword) {
    const term = allTerms.find(t => t.keyword.toLowerCase() === keyword.toLowerCase());
    if (term) {
        // Загрузить полное определение
        fetch(`${API_BASE}/terms/${keyword}`)
            .then(r => r.json())
            .then(term => {
                const card = document.querySelector(`[data-keyword="${keyword}"]`);
                if (card) {
                    const defEl = card.querySelector('.term-definition');
                    if (defEl) {
                        defEl.textContent = term.definition;
                    }
                }
            })
            .catch(() => {});
    }
    return 'Загрузка...';
}

function filterTerms() {
    const search = document.getElementById('search-input').value.toLowerCase();
    const category = document.getElementById('category-filter').value;
    
    let filtered = allTerms;
    
    if (search) {
        filtered = filtered.filter(term => 
            term.keyword.toLowerCase().includes(search) ||
            term.title.toLowerCase().includes(search)
        );
    }
    
    if (category) {
        filtered = filtered.filter(term => term.category === category);
    }
    
    renderTerms(filtered);
}

function updateCategoryFilter() {
    const categories = [...new Set(allTerms.map(t => t.category).filter(Boolean))].sort();
    const select = document.getElementById('category-filter');
    const currentValue = select.value;
    
    select.innerHTML = '<option value="">Все категории</option>' +
        categories.map(cat => `<option value="${escapeHtml(cat)}">${escapeHtml(cat)}</option>`).join('');
    
    if (categories.includes(currentValue)) {
        select.value = currentValue;
    }
}

// Граф
function initializeGraph() {
    const refreshBtn = document.getElementById('refresh-graph-btn');
    refreshBtn.addEventListener('click', loadGraph);
}

async function loadGraph() {
    try {
        const response = await fetch(`${API_BASE}/graph`);
        const data = await response.json();
        
        updateGraphStats(data);
        renderGraph(data);
    } catch (error) {
        console.error('Ошибка загрузки графа:', error);
        alert('Ошибка загрузки графа');
    }
}

function updateGraphStats(data) {
    const stats = document.getElementById('graph-stats');
    stats.textContent = `Узлов: ${data.nodes.length}, Связей: ${data.edges.length}`;
}

function renderGraph(data) {
    const container = document.getElementById('graph-container');
    
    console.log('Graph data received:', data);
    console.log('Nodes count:', data.nodes?.length || 0);
    console.log('Edges count:', data.edges?.length || 0);
    if (data.edges && data.edges.length > 0) {
        console.log('First edge sample:', data.edges[0]);
    }
    
    // Подготовка данных для vis-network
    const nodesData = data.nodes.map(node => ({
        id: node.id,
        label: node.title,
        title: `${node.title}\n\n${node.definition}\n\n${node.source ? `Источник: ${node.source}` : ''}`,
        group: node.category || 'Другое',
        color: getCategoryColor(node.category)
    }));
    
    const edgesData = data.edges.map((edge, index) => {
        // Поддержка обоих форматов: с алиасами (from/to) и без (from_id/to_id)
        const fromId = edge.from !== undefined ? edge.from : (edge.from_id !== undefined ? edge.from_id : null);
        const toId = edge.to !== undefined ? edge.to : (edge.to_id !== undefined ? edge.to_id : null);
        
        if (!fromId || !toId) {
            console.warn('Invalid edge at index', index, ':', edge);
            return null;
        }
        
        // Проверяем, что узлы существуют
        const fromNodeExists = nodesData.some(n => n.id === fromId);
        const toNodeExists = nodesData.some(n => n.id === toId);
        
        if (!fromNodeExists || !toNodeExists) {
            console.warn('Edge references non-existent node:', { fromId, toId, fromExists: fromNodeExists, toExists: toNodeExists });
            return null;
        }
        
        return {
            id: `edge_${fromId}_${toId}_${index}`,
            from: fromId,
            to: toId,
            label: edge.label || '',
            arrows: 'to',
            color: { color: '#666' },
            width: 2
        };
    }).filter(edge => edge !== null);
    
    console.log('Processed edges:', edgesData);
    
    const graphData = {
        nodes: new vis.DataSet(nodesData),
        edges: new vis.DataSet(edgesData)
    };
    
    const options = {
        nodes: {
            shape: 'dot',
            size: 20,
            font: {
                size: 14,
                color: '#333'
            },
            borderWidth: 2,
            shadow: true
        },
        edges: {
            width: 3,
            color: {
                color: '#666',
                highlight: '#333'
            },
            smooth: {
                type: 'continuous',
                roundness: 0.5
            },
            arrows: {
                to: {
                    enabled: true,
                    scaleFactor: 1.2
                }
            },
            font: {
                size: 10,
                align: 'middle',
                color: '#666'
            },
            selectionWidth: 4
        },
        physics: {
            enabled: true,
            stabilization: {
                iterations: 200
            },
            barnesHut: {
                gravitationalConstant: -2000,
                centralGravity: 0.1,
                springLength: 200,
                springConstant: 0.04
            }
        },
        interaction: {
            hover: true,
            tooltipDelay: 100,
            zoomView: true,
            dragView: true
        }
    };
    
    if (network) {
        network.destroy();
    }
    
    network = new vis.Network(container, graphData, options);
    
    // Обработчик клика на узел
    network.on('click', (params) => {
        if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            const node = data.nodes.find(n => n.id === nodeId);
            if (node) {
                viewTerm(node.id);
            }
        }
    });
}

function getCategoryColor(category) {
    const colors = {
        'Концепция': '#3498DB',
        'Технология': '#4A90E2',
        'Архитектура': '#9B59B6',
        'API': '#F39C12',
        'Функциональность': '#E74C3C',
        'Дизайн': '#1ABC9C',
        'Безопасность': '#E91E63',
        'Инструмент': '#34495E',
        'Характеристика': '#50C878',
        'Конфигурация': '#607D8B',
    };
    return colors[category] || '#95A5A6';
}

// Модальные окна
function initializeModals() {
    const modal = document.getElementById('term-modal');
    const viewModal = document.getElementById('view-term-modal');
    const form = document.getElementById('term-form');
    
    document.querySelector('.close').addEventListener('click', closeTermModal);
    document.querySelector('.close-view').addEventListener('click', closeViewModal);
    document.getElementById('cancel-btn').addEventListener('click', closeTermModal);
    
    form.addEventListener('submit', handleFormSubmit);
    
    // Закрытие по клику вне модального окна
    window.addEventListener('click', (e) => {
        if (e.target === modal) closeTermModal();
        if (e.target === viewModal) closeViewModal();
    });
}

function openTermModal(keyword = null) {
    const modal = document.getElementById('term-modal');
    const form = document.getElementById('term-form');
    const title = document.getElementById('modal-title');
    
    form.reset();
    document.getElementById('term-keyword-edit').value = '';
    
    if (keyword) {
        title.textContent = 'Редактировать термин';
        loadTermForEdit(keyword);
    } else {
        title.textContent = 'Добавить термин';
        document.getElementById('term-keyword').disabled = false;
    }
    
    modal.classList.add('active');
}

function closeTermModal() {
    document.getElementById('term-modal').classList.remove('active');
}

async function loadTermForEdit(keyword) {
    try {
        const response = await fetch(`${API_BASE}/terms/${keyword}`);
        const term = await response.json();
        
        document.getElementById('term-keyword-edit').value = term.keyword;
        document.getElementById('term-keyword').value = term.keyword;
        document.getElementById('term-title').value = term.title;
        document.getElementById('term-definition').value = term.definition;
        document.getElementById('term-source').value = term.source || '';
        document.getElementById('term-category').value = term.category || '';
        document.getElementById('term-related').value = term.related_terms.join(', ');
        
        document.getElementById('term-keyword').disabled = true;
    } catch (error) {
        console.error('Ошибка загрузки термина:', error);
        alert('Ошибка загрузки термина');
    }
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    const keywordEdit = document.getElementById('term-keyword-edit').value;
    const isEdit = !!keywordEdit;
    
    const termData = {
        keyword: document.getElementById('term-keyword').value,
        title: document.getElementById('term-title').value,
        definition: document.getElementById('term-definition').value,
        source: document.getElementById('term-source').value || null,
        category: document.getElementById('term-category').value || null,
        related_terms: document.getElementById('term-related').value
            .split(',')
            .map(s => s.trim())
            .filter(Boolean)
    };
    
    try {
        let response;
        if (isEdit) {
            // Обновление
            const updateData = { ...termData };
            delete updateData.keyword;
            response = await fetch(`${API_BASE}/terms/${keywordEdit}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updateData)
            });
        } else {
            // Создание
            response = await fetch(`${API_BASE}/terms`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(termData)
            });
        }
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Ошибка сохранения');
        }
        
        closeTermModal();
        await loadTerms();
        if (currentView === 'graph') {
            await loadGraph();
        }
    } catch (error) {
        alert(error.message || 'Ошибка сохранения термина');
    }
}

async function viewTerm(keyword) {
    try {
        const response = await fetch(`${API_BASE}/terms/${keyword}`);
        const term = await response.json();
        
        const relatedTermsHtml = term.related_terms.length > 0
            ? `<div class="term-related">
                <h3>Связанные термины:</h3>
                <div class="related-terms">
                    ${term.related_terms.map(rt => 
                        `<a href="#" class="related-term-tag" onclick="event.preventDefault(); viewTerm('${rt}'); closeViewModal();">${rt}</a>`
                    ).join('')}
                </div>
              </div>`
            : '';
        
        document.getElementById('term-details').innerHTML = `
            <div class="term-title">${escapeHtml(term.title)}</div>
            <div class="term-keyword">${escapeHtml(term.keyword)}</div>
            ${term.category ? `<div><span class="term-category">${escapeHtml(term.category)}</span></div>` : ''}
            <div class="term-definition">${escapeHtml(term.definition)}</div>
            ${term.source ? `<div class="term-source">Источник: <a href="${escapeHtml(term.source)}" target="_blank">${escapeHtml(term.source)}</a></div>` : ''}
            ${relatedTermsHtml}
            <div class="form-actions" style="margin-top: 30px;">
                <button class="btn-edit" onclick="editTerm('${term.keyword}'); closeViewModal();">Редактировать</button>
                <button class="btn-delete" onclick="deleteTerm('${term.keyword}'); closeViewModal();">Удалить</button>
            </div>
        `;
        
        document.getElementById('view-term-modal').classList.add('active');
    } catch (error) {
        console.error('Ошибка загрузки термина:', error);
        alert('Ошибка загрузки термина');
    }
}

function closeViewModal() {
    document.getElementById('view-term-modal').classList.remove('active');
}

async function editTerm(keyword) {
    openTermModal(keyword);
}

async function deleteTerm(keyword) {
    if (!confirm(`Вы уверены, что хотите удалить термин "${keyword}"?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/terms/${keyword}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Ошибка удаления');
        }
        
        await loadTerms();
        if (currentView === 'graph') {
            await loadGraph();
        }
    } catch (error) {
        alert('Ошибка удаления термина');
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
