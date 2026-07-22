import os
import re

html1_target = """                div.innerHTML = `
                    <div class="status-dot ${activeCls}"></div>
                    <div class="text-truncate fw-semibold" style="max-width: 140px;">${tal.name}</div>
                    <div class="tal-actions dropdown ms-auto" onclick="event.stopPropagation();">
                        <button class="btn btn-link btn-sm text-white-50 p-0" data-bs-toggle="dropdown"><i class="fa-solid fa-ellipsis-vertical px-2"></i></button>
                        <ul class="dropdown-menu dropdown-menu-glass dropdown-menu-end shadow" style="font-size: 12px;">
                            <li><a class="dropdown-item d-flex justify-content-between align-items-center toggle-active" href="#">Activate <div class="form-check form-switch m-0"><input class="form-check-input" type="checkbox" ${tal.active?'checked':''}></div></a></li>
                            <li><hr class="dropdown-divider border-secondary"></li>
                            <li><a class="dropdown-item clone-tal" href="#"><i class="fa-solid fa-clone me-2 text-info w-15px"></i> Duplicate</a></li>
                            <li><a class="dropdown-item edit-tal" href="#"><i class="fa-solid fa-pen-nib me-2 text-warning w-15px"></i> Rename</a></li>
                            <li><a class="dropdown-item save-tal" href="#"><i class="fa-solid fa-microchip me-2 text-success w-15px"></i> Save Filters</a></li>
                            <li><hr class="dropdown-divider border-secondary"></li>
                            <li><a class="dropdown-item text-danger delete-tal" href="#"><i class="fa-solid fa-skull me-2 w-15px"></i> Delete</a></li>
                        </ul>
                    </div>
                `;

                div.addEventListener('click', () => {
                    if (selectedTalId === tal.id) selectedTalId = null; 
                    else {
                        selectedTalId = tal.id;
                        if (tal.savedFilters) loadSavedFilters(tal.savedFilters);
                    }
                    renderTals();
                    applyFilterEngine();
                });

                const menu = div.querySelector('.dropdown-menu');
                menu.querySelector('.toggle-active').addEventListener('click', (e) => {
                    e.preventDefault(); e.stopPropagation();
                    talLists[index].active = !talLists[index].active;
                    renderTals(); applyFilterEngine();
                });
                menu.querySelector('.clone-tal').addEventListener('click', (e) => {"""

html1_replace = """                div.innerHTML = `
                    <div class="form-check form-switch m-0 me-2" onclick="event.stopPropagation();" title="Toggle Active Status">
                        <input class="form-check-input tal-active-toggle" type="checkbox" style="cursor: pointer; margin-top: 0.15rem;" ${tal.active ? 'checked' : ''}>
                    </div>
                    <div class="text-truncate fw-semibold" style="max-width: 140px;">${tal.name}</div>
                    <div class="tal-actions dropdown ms-auto" onclick="event.stopPropagation();">
                        <button class="btn btn-link btn-sm text-white-50 p-0" data-bs-toggle="dropdown"><i class="fa-solid fa-ellipsis-vertical px-2"></i></button>
                        <ul class="dropdown-menu dropdown-menu-glass dropdown-menu-end shadow" style="font-size: 12px;">
                            <li><a class="dropdown-item clone-tal" href="#"><i class="fa-solid fa-clone me-2 text-info w-15px"></i> Duplicate</a></li>
                            <li><a class="dropdown-item edit-tal" href="#"><i class="fa-solid fa-pen-nib me-2 text-warning w-15px"></i> Rename</a></li>
                            <li><a class="dropdown-item save-tal" href="#"><i class="fa-solid fa-microchip me-2 text-success w-15px"></i> Save Filters</a></li>
                            <li><hr class="dropdown-divider border-secondary"></li>
                            <li><a class="dropdown-item text-danger delete-tal" href="#"><i class="fa-solid fa-skull me-2 w-15px"></i> Delete</a></li>
                        </ul>
                    </div>
                `;

                div.addEventListener('click', () => {
                    if (selectedTalId === tal.id) selectedTalId = null; 
                    else {
                        selectedTalId = tal.id;
                        if (tal.savedFilters) loadSavedFilters(tal.savedFilters);
                    }
                    renderTals();
                    applyFilterEngine();
                });

                div.querySelector('.tal-active-toggle').addEventListener('change', (e) => {
                    e.stopPropagation();
                    talLists[index].active = e.target.checked;
                    renderTals(); applyFilterEngine();
                });

                const menu = div.querySelector('.dropdown-menu');
                menu.querySelector('.clone-tal').addEventListener('click', (e) => {"""

html2_target = html1_target.replace('text-white-50', 'text-dark-50')
html2_replace = html1_replace.replace('text-white-50', 'text-dark-50')

files = [
    ('c:/Users/CW251005/Desktop/Launchpad/index1.html', html1_target, html1_replace),
    ('c:/Users/CW251005/Desktop/Launchpad/index2.html', html2_target, html2_replace)
]

for filepath, target, replacement in files:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace(target, replacement)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print("TAL List layout updated")
