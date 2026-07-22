import re
import os

files = [
    ('c:/Users/CW251005/Desktop/Launchpad/index1.html', 'btn-outline-light', 'text-white'),
    ('c:/Users/CW251005/Desktop/Launchpad/index2.html', 'btn-outline-dark', 'text-dark')
]

for filepath, btn_outline, text_color in files:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        replacement = f"""                <div id="addTalForm" class="d-none mb-3 p-3 glass-inner shadow-sm rounded-3">
                    <label class="form-label small fw-bold {{text_color}} mb-2"><i class="fa-solid fa-folder-plus me-1 text-primary"></i> Create New List</label>
                    <div class="input-group input-group-sm mb-2">
                        <input type="text" class="form-control form-control-glass" id="newTalNameInput" placeholder="Enter list name...">
                    </div>
                    <div class="d-flex justify-content-end gap-2 mt-2">
                        <button class="btn btn-sm {{btn_outline}} py-1" id="cancelTalBtn" type="button" style="font-size:11px"><i class="fa-solid fa-xmark me-1"></i> Cancel</button>
                        <button class="btn btn-sm btn-glow py-1 px-3 fw-bold" id="saveTalBtn" type="button" style="font-size:11px"><i class="fa-solid fa-check me-1"></i> Save</button>
                    </div>
                </div>"""
        replacement = replacement.replace('{{text_color}}', text_color).replace('{{btn_outline}}', btn_outline)
        
        # Use regex to replace the old block
        content = re.sub(
            r'<div id="addTalForm" class="d-none mb-3">.*?</div>\s+</div>',
            replacement,
            content,
            flags=re.DOTALL
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print("Replacement complete.")
