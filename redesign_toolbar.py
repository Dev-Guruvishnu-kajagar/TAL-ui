import os
import re

html_template = """        <!-- Filter Bar -->
        <div class="glass-panel p-3 mb-3">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h6 class="mb-0 fw-bold {title_color}"><i class="fa-solid fa-microchip me-2" style="color: var(--neon-cyan)"></i> TAL Config</h6>
                <div class="d-flex gap-2">
                    <button class="btn btn-sm {btn_outline} fw-semibold px-3 rounded-pill" style="height:28px; line-height:1;" id="resetBtn">Reset All</button>
                    <button class="btn btn-sm btn-glow fw-bold px-4 rounded-pill shadow-sm" style="height:28px; line-height:1;" id="applyBtn">Fetch TAL</button>
                </div>
            </div>

            <!-- Compact UI Layout -->
            <div class="d-flex flex-wrap gap-2 align-items-center">
                
                <!-- Modes Group -->
                <div class="glass-inner p-1 px-3 d-flex gap-3 align-items-center rounded-pill">
                    <div class="d-flex align-items-center gap-2">
                        <span class="filter-label mb-0" style="font-size:10px;">Email</span>
                        <div class="compact-toggle" style="width: 60px;">
                            <input type="radio" name="emailMode" id="emInclude" value="Include" checked>
                            <label for="emInclude" style="font-size:9px;">Inc</label>
                            <input type="radio" name="emailMode" id="emExclude" value="Exclude">
                            <label for="emExclude" style="font-size:9px;">Exc</label>
                        </div>
                    </div>
                    <div class="d-flex align-items-center gap-2">
                        <span class="filter-label mb-0" style="font-size:10px;">Domain</span>
                        <div class="compact-toggle" style="width: 60px;">
                            <input type="radio" name="domainMode" id="domInclude" value="Include" checked>
                            <label for="domInclude" style="font-size:9px;">Inc</label>
                            <input type="radio" name="domainMode" id="domExclude" value="Exclude">
                            <label for="domExclude" style="font-size:9px;">Exc</label>
                        </div>
                    </div>
                    <div class="d-flex align-items-center gap-2">
                        <span class="filter-label mb-0" style="font-size:10px;">Company</span>
                        <div class="compact-toggle" style="width: 60px;">
                            <input type="radio" name="companyMode" id="compInclude" value="Include" checked>
                            <label for="compInclude" style="font-size:9px;">Inc</label>
                            <input type="radio" name="companyMode" id="compExclude" value="Exclude">
                            <label for="compExclude" style="font-size:9px;">Exc</label>
                        </div>
                    </div>
                </div>

                <!-- Geo & CPC Group -->
                <div class="glass-inner p-1 px-3 d-flex gap-3 align-items-center rounded-pill">
                    <div class="d-flex align-items-center gap-2">
                        <span class="filter-label mb-0" style="font-size:10px;">Geo</span>
                        <select class="form-select form-control-glass px-2 py-0" style="height:22px; font-size:10px; width:auto;" id="geoMode">
                            <option value="Include">In</option>
                            <option value="Exclude">Ex</option>
                        </select>
                        <input type="text" class="form-control form-control-glass px-2 py-0 shadow-none" style="height:22px; font-size:10px; width:90px;" id="geoInput" placeholder="US, CA...">
                    </div>
                    <div class="d-flex align-items-center gap-2 border-start {border_class} ps-3">
                        <span class="filter-label mb-0" style="font-size:10px;">CPC</span>
                        <select class="form-select form-control-glass px-2 py-0" style="height:22px; font-size:10px; width:auto;" id="cpcMode">
                            <option value="Include">In</option>
                            <option value="Exclude">Ex</option>
                        </select>
                        <input type="number" class="form-control form-control-glass px-2 py-0 shadow-none" style="height:22px; font-size:10px; width:70px;" id="cpcInput" placeholder="Value">
                    </div>
                </div>

                <!-- Priority & Status Group -->
                <div class="glass-inner p-1 px-3 d-flex gap-3 align-items-center rounded-pill">
                    <div class="d-flex align-items-center gap-2">
                        <span class="filter-label mb-0" style="font-size:10px;">Priority</span>
                        <input type="number" class="form-control form-control-glass px-1 py-0 shadow-none" style="height:22px; font-size:10px; width:45px; text-align:center" id="priMin" min="1" max="10" placeholder="Min">
                        <span class="text-muted" style="font-size:10px;">-</span>
                        <input type="number" class="form-control form-control-glass px-1 py-0 shadow-none" style="height:22px; font-size:10px; width:45px; text-align:center" id="priMax" min="1" max="10" placeholder="Max">
                    </div>
                    <div class="d-flex align-items-center gap-2 border-start {border_class} ps-3">
                        <span class="filter-label mb-0" style="font-size:10px;">ABM</span>
                        <div class="segmented-control p-0" style="height:22px; border:none; background:transparent;">
                            <input type="radio" name="abmFilter" id="abmAll" value="All" checked>
                            <label for="abmAll" class="{abm_label_bg} rounded-pill" style="font-size:10px; padding: 2px 8px; margin:0; line-height:16px;">All</label>
                            <input type="radio" name="abmFilter" id="abmTarget" value="Target">
                            <label for="abmTarget" class="{abm_label_bg} rounded-pill mx-1" style="font-size:10px; padding: 2px 8px; margin:0; line-height:16px;">Target</label>
                            <input type="radio" name="abmFilter" id="abmNotTarget" value="DoNotTarget">
                            <label for="abmNotTarget" class="{abm_label_bg} rounded-pill" style="font-size:10px; padding: 2px 8px; margin:0; line-height:16px;">None</label>
                        </div>
                    </div>
                </div>

                <!-- Stage Dropdown Group -->
                <div class="glass-inner p-1 px-3 d-flex align-items-center rounded-pill">
                    <span class="filter-label mb-0 me-2" style="font-size:10px;">Stage</span>
                    <div class="dropdown">
                        <button class="btn d-flex justify-content-between align-items-center form-control-glass px-2 py-0 shadow-none" style="height:22px; font-size:10px; width:130px; background: rgba(0,0,0,0.05);" type="button" data-bs-toggle="dropdown" data-bs-auto-close="outside">
                            <span id="stageBtnText" class="text-truncate">All Stages</span>
                            <i class="fa-solid fa-chevron-down ms-2 text-muted" style="font-size: 8px;"></i>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-glass p-2 shadow" style="font-size: 11px;">
                            <li><div class="form-check ms-2 mb-1"><input class="form-check-input stage-cb bg-white border-secondary" type="checkbox" value="Awareness" id="stg1"><label class="form-check-label" for="stg1">Awareness</label></div></li>
                            <li><div class="form-check ms-2 mb-1"><input class="form-check-input stage-cb bg-white border-secondary" type="checkbox" value="Consideration" id="stg2"><label class="form-check-label" for="stg2">Consideration</label></div></li>
                            <li><div class="form-check ms-2 mb-1"><input class="form-check-input stage-cb bg-white border-secondary" type="checkbox" value="Decision" id="stg3"><label class="form-check-label" for="stg3">Decision</label></div></li>
                            <li><div class="form-check ms-2 mb-2"><input class="form-check-input stage-cb bg-white border-secondary" type="checkbox" value="Interest" id="stg4"><label class="form-check-label" for="stg4">Interest</label></div></li>
                            <li><hr class="dropdown-divider border-secondary my-1"></li>
                            <li><a class="dropdown-item text-danger text-center fw-bold rounded" href="#" id="clearStagesBtn" style="padding: 2px 0;">Clear</a></li>
                        </ul>
                    </div>
                </div>

            </div>
        </div>"""

files = [
    ('c:/Users/CW251005/Desktop/Launchpad/index1.html', 'text-white', 'btn-outline-light', 'border-secondary', 'bg-dark'),
    ('c:/Users/CW251005/Desktop/Launchpad/index2.html', 'text-dark', 'btn-outline-dark', 'border-light', 'bg-white')
]

for filepath, title_color, btn_outline, border_class, abm_label_bg in files:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        html_formatted = html_template.format(
            title_color=title_color,
            btn_outline=btn_outline,
            border_class=border_class,
            abm_label_bg=abm_label_bg
        )

        content = re.sub(
            r'<!-- Filter Bar -->.*?</div>\s+<!-- Data Table -->',
            html_formatted + '\n\n        <!-- Data Table -->',
            content,
            flags=re.DOTALL
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print("Toolbar redesigned.")
