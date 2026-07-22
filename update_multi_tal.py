import os

def update_file(filepath):
    if not os.path.exists(filepath):
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update State
    content = content.replace("let selectedTalId = null;", "let currentTab = 'Mix';")

    # 2. Add Tab HTML above table
    tab_html = """
        <!-- Data Table -->
        <div class="glass-panel table-container">
            <!-- New Tab Navigation -->
            <ul class="nav nav-tabs border-0 px-3 pt-3 mb-0" id="dataTabs" role="tablist" style="background: rgba(0,0,0,0.02); border-bottom: 1px solid rgba(0,0,0,0.05) !important;">
                <li class="nav-item" role="presentation">
                    <button class="nav-link active fw-bold" id="mix-tab" data-bs-toggle="tab" data-tab-value="Mix" type="button" role="tab" style="border: none; border-bottom: 2px solid transparent; background: transparent; color: var(--text-main); font-size: 13px; padding-bottom: 12px;">Mix Active TALs</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link fw-bold" id="filtered-tab" data-bs-toggle="tab" data-tab-value="Filtered" type="button" role="tab" style="border: none; border-bottom: 2px solid transparent; background: transparent; color: var(--text-muted); font-size: 13px; padding-bottom: 12px;">Filtered Data</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link fw-bold" id="custom-tab" data-bs-toggle="tab" data-tab-value="Custom" type="button" role="tab" style="border: none; border-bottom: 2px solid transparent; background: transparent; color: var(--text-muted); font-size: 13px; padding-bottom: 12px;">Customizable</button>
                </li>
            </ul>
            <div class="table-responsive">"""
    
    content = content.replace("""        <!-- Data Table -->
        <div class="glass-panel table-container">
            <div class="table-responsive">""", tab_html)

    # 3. Add Tab CSS
    tab_css = """
        .nav-tabs .nav-link.active {
            border-bottom: 2px solid var(--neon-cyan) !important;
            color: var(--neon-cyan) !important;
        }
        .nav-tabs .nav-link:hover:not(.active) {
            border-bottom: 2px solid rgba(0, 243, 255, 0.3) !important;
            color: var(--text-main) !important;
        }
"""
    if "nav-tabs .nav-link" not in content:
        content = content.replace("/* --- Data Table --- */", "/* --- Data Table --- */" + tab_css)

    # 4. Bind Tabs in init/bindEvents
    bind_tabs_js = """
            // Bind Tabs
            const tabBtns = document.querySelectorAll('#dataTabs .nav-link');
            tabBtns.forEach(btn => {
                btn.addEventListener('click', (e) => {
                    tabBtns.forEach(b => {
                        b.classList.remove('active');
                        b.style.color = 'var(--text-muted)';
                    });
                    e.target.classList.add('active');
                    e.target.style.color = 'var(--neon-cyan)';
                    currentTab = e.target.getAttribute('data-tab-value');
                    applyFilterEngine();
                });
            });

            // Controls"""
    content = content.replace("// Controls", bind_tabs_js)

    # 5. Fix Reset logic
    content = content.replace("selectedTalId = null;", "currentTab = 'Mix'; document.getElementById('mix-tab').click();")

    # 6. Rewrite applyFilterEngine
    old_apply_logic = """        function applyFilterEngine() {
            // 1. Row Visibility
            const sideAbm = getRadioVal(els.sideTalAbm);
            const sideStatus = getRadioVal(els.sideTalStatus);
            
            let visibleLeads = dummyLeads.filter(l => {
                if (sideAbm === 'No' && l.abm === 'Target') return false;
                if (sideStatus === 'Inactive' && l.priority > 2) return false;
                
                if (selectedTalId) {
                    const activeTal = talLists.find(t => t.id === selectedTalId && t.active);
                    if (activeTal && !activeTal.leads.includes(l.domain)) return false;
                }
                return true;
            });"""

    new_apply_logic = """        function applyFilterEngine() {
            const activeTals = talLists.filter(t => t.active);
            const mixTabBtn = document.getElementById('mix-tab');
            if(mixTabBtn) {
                if(activeTals.length === 0) mixTabBtn.innerText = "Mix Active TALs (0)";
                else if(activeTals.length <= 2) mixTabBtn.innerText = "Mix: " + activeTals.map(t => t.name).join(' & ');
                else mixTabBtn.innerText = `Mix Active TALs (${activeTals.length})`;
            }

            // 1. Row Visibility
            const sideAbm = getRadioVal(els.sideTalAbm);
            const sideStatus = getRadioVal(els.sideTalStatus);
            
            const activeDomains = new Set();
            activeTals.forEach(t => t.leads.forEach(d => activeDomains.add(d)));

            let visibleLeads = dummyLeads.filter(l => {
                if (activeTals.length > 0 && !activeDomains.has(l.domain)) return false;
                if (sideAbm === 'No' && l.abm === 'Target') return false;
                if (sideStatus === 'Inactive' && l.priority > 2) return false;
                return true;
            });"""
    content = content.replace(old_apply_logic, new_apply_logic)

    # 7. Apply Strict Filtering for Tabs inside applyFilterEngine
    # It currently has:
    #             // 2. Highlighting
    #             const ctx = getHighlightContext();
    #             const rulesActive = hasAnyHighlightRuleActive(ctx);
    #
    #             renderRows(visibleLeads, ctx, rulesActive);
    
    old_render = """            // 2. Highlighting
            const ctx = getHighlightContext();
            const rulesActive = hasAnyHighlightRuleActive(ctx);

            renderRows(visibleLeads, ctx, rulesActive);"""
            
    new_render = """            // 2. Highlighting
            const ctx = getHighlightContext();
            const rulesActive = hasAnyHighlightRuleActive(ctx);

            if (currentTab === 'Filtered') {
                visibleLeads = visibleLeads.filter(l => passesHighlightFilters(l, ctx));
            } else if (currentTab === 'Custom') {
                visibleLeads = visibleLeads.filter(l => l.priority === 1); // Placeholder custom logic
            }

            renderRows(visibleLeads, ctx, rulesActive);"""
    content = content.replace(old_render, new_render)

    # 8. Fix renderTals click listener
    old_row_click = """                div.addEventListener('click', () => {
                    if (selectedTalId === tal.id) selectedTalId = null; 
                    else {
                        selectedTalId = tal.id;
                        if (tal.savedFilters) loadSavedFilters(tal.savedFilters);
                    }
                    renderTals();
                    applyFilterEngine();
                });"""
    
    new_row_click = """                div.addEventListener('click', () => {
                    talLists[index].active = !talLists[index].active;
                    if (talLists[index].active && tal.savedFilters) loadSavedFilters(tal.savedFilters);
                    renderTals();
                    applyFilterEngine();
                });"""
    content = content.replace(old_row_click, new_row_click)
    
    # 9. Fix renderTals selection styling (we don't have single selection anymore, but we can highlight based on active)
    content = content.replace("const isSelected = selectedTalId === tal.id;", "const isSelected = tal.active;")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

files = [
    'c:/Users/CW251005/Desktop/Launchpad/index1.html',
    'c:/Users/CW251005/Desktop/Launchpad/index2.html'
]
for f in files:
    update_file(f)

print("Tabs and active combination logic successfully injected.")
