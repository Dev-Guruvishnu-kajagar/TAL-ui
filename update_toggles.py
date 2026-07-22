import os
import re

files = [
    ('c:/Users/CW251005/Desktop/Launchpad/index1.html', 'rgba(255,255,255,0.05)', 'rgba(255,255,255,0.1)', 'border-secondary'),
    ('c:/Users/CW251005/Desktop/Launchpad/index2.html', 'rgba(0,0,0,0.05)', '#fff', 'border-light')
]

for filepath, bg_color, checked_bg, border_class in files:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. Add CSS for compact-toggle
        css_block = f"""
        .compact-toggle {{
            display: flex;
            background: {bg_color};
            border-radius: 12px;
            padding: 2px;
            border: 1px solid {bg_color};
            width: 80px;
        }}
        .compact-toggle input[type="radio"] {{ display: none; }}
        .compact-toggle label {{
            flex: 1; text-align: center; padding: 2px 0;
            font-size: 10px; font-weight: 700; cursor: pointer;
            border-radius: 10px; transition: all 0.3s;
            color: var(--text-muted); margin: 0;
        }}
        .compact-toggle input[type="radio"]:checked + label {{
            background: {checked_bg};
            color: var(--text-main);
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
"""
        if '.compact-toggle {' not in content:
            content = content.replace('/* Form Inputs */', css_block + '\n        /* Form Inputs */')

        # 2. Replace HTML for Col 1
        html_block = f"""                <!-- Col 1 -->
                <div class="col-md-6 col-xl-3">
                    <div class="glass-inner p-3 h-100 d-flex flex-column gap-3">
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="filter-label mb-0">Email Mode</span>
                            <div class="compact-toggle">
                                <input type="radio" name="emailMode" id="emInclude" value="Include" checked>
                                <label for="emInclude">Inc</label>
                                <input type="radio" name="emailMode" id="emExclude" value="Exclude">
                                <label for="emExclude">Exc</label>
                            </div>
                        </div>
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="filter-label mb-0">Domain Mode</span>
                            <div class="compact-toggle">
                                <input type="radio" name="domainMode" id="domInclude" value="Include" checked>
                                <label for="domInclude">Inc</label>
                                <input type="radio" name="domainMode" id="domExclude" value="Exclude">
                                <label for="domExclude">Exc</label>
                            </div>
                        </div>
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="filter-label mb-0">Company Name Mode</span>
                            <div class="compact-toggle">
                                <input type="radio" name="companyMode" id="compInclude" value="Include" checked>
                                <label for="compInclude">Inc</label>
                                <input type="radio" name="companyMode" id="compExclude" value="Exclude">
                                <label for="compExclude">Exc</label>
                            </div>
                        </div>
                        
                        <div class="mt-auto border-top {border_class} pt-2 text-center" style="opacity: 0.6">
                            <span class="small fw-semibold" style="font-size:10px;"><i class="fa-solid fa-plus text-primary me-1"></i> Expansion Area</span>
                        </div>
                    </div>
                </div>"""

        # Replace the entire Col 1
        content = re.sub(
            r'<!-- Col 1 -->.*?<!-- Col 2 -->',
            html_block + '\n\n                <!-- Col 2 -->',
            content,
            flags=re.DOTALL
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print("Toggles updated.")
