type ObservationRow = {
    id: string;
    species: string;
    time: string;
    region: string;
    visibility: string;
    status: string;
};


const observationRows: ObservationRow[] = [
    {
        id: "OBS-0007",
        species: "ヒヨドリ候補",
        time: "2026-04-18 06:42 JST",
        region: "Kanto West",
        visibility: "Masked",
        status: "Review pending",
    },
    {
        id: "OBS-0006",
        species: "Unknown passerine",
        time: "2026-04-18 05:58 JST",
        region: "Kanto North",
        visibility: "Public",
        status: "Analyzed",
    },
    {
        id: "OBS-0005",
        species: "アオゲラ候補",
        time: "2026-04-17 18:11 JST",
        region: "Chubu East",
        visibility: "Restricted",
        status: "Masked",
    },
];


const states = [
    { label: "Normal", tone: "normal", detail: "Observation list and inspector are available." },
    { label: "Loading", tone: "loading", detail: "Refreshing observation rows from the API." },
    { label: "Empty", tone: "empty", detail: "No observations matched the current filters." },
    { label: "Error", tone: "error", detail: "Observation data could not be loaded." },
    { label: "Offline", tone: "offline", detail: "Cached workspace only. Sync is paused." },
    { label: "Success", tone: "success", detail: "Masking rules were applied successfully." },
    { label: "Permission", tone: "permission", detail: "Protected coordinates are hidden for this role." },
] as const;


const sidebarSections = [
    {
        title: "Workspace",
        items: ["Dashboard", "Observations", "Map", "Review Queue"],
    },
    {
        title: "Sources",
        items: ["Recent Imports", "Local Demo Set", "Masked Exports"],
    },
];


export function WorkspaceShell() {
    return (
        <div className="workspace-root">
            <a className="skip-link" href="#main-content">
                メインコンテンツへ移動
            </a>

            <header className="toolbar" aria-label="Primary toolbar">
                <div className="toolbar__group toolbar__group--title">
                    <span className="toolbar__product">EcoAudio Mapper</span>
                    <h1 className="toolbar__heading">Observation Workspace</h1>
                </div>

                <div className="toolbar__group" role="group" aria-label="Primary actions">
                    <button type="button" className="toolbar__button">
                        Import Video
                    </button>
                    <button type="button" className="toolbar__button toolbar__button--active" aria-pressed="true">
                        Review Queue
                    </button>
                    <button type="button" className="toolbar__button">
                        Refresh
                    </button>
                </div>
            </header>

            <div className="workspace-grid">
                <aside className="sidebar" aria-label="Primary navigation">
                    {sidebarSections.map((section) => (
                        <section key={section.title} className="sidebar__section" aria-labelledby={`nav-${section.title}`}>
                            <h2 id={`nav-${section.title}`} className="sidebar__heading">
                                {section.title}
                            </h2>
                            <ul className="sidebar__list">
                                {section.items.map((item, index) => (
                                    <li key={item}>
                                        <button
                                            type="button"
                                            className={`sidebar__item${section.title === "Workspace" && index === 1 ? " is-selected" : ""}`}
                                            aria-current={section.title === "Workspace" && index === 1 ? "page" : undefined}
                                        >
                                            {item}
                                        </button>
                                    </li>
                                ))}
                            </ul>
                        </section>
                    ))}
                </aside>

                <main id="main-content" className="main-pane">
                    <section className="overview" aria-labelledby="overview-title">
                        <div>
                            <p className="eyebrow">Current focus</p>
                            <h2 id="overview-title" className="section-title">
                                Observation review queue
                            </h2>
                        </div>
                        <p className="overview__summary">
                            Review candidate detections, verify masking state, and inspect observation metadata in a compact desktop layout.
                        </p>
                    </section>

                    <section className="state-strip" aria-labelledby="workspace-states-title">
                        <div className="state-strip__header">
                            <h2 id="workspace-states-title" className="section-title">
                                Operational states
                            </h2>
                            <p className="state-strip__summary">The first slice makes required states explicit without adding decorative cards.</p>
                        </div>
                        <ul className="state-strip__list">
                            {states.map((state) => (
                                <li key={state.label} className={`state-pill state-pill--${state.tone}`}>
                                    <span className="state-pill__label">{state.label}</span>
                                    <span className="state-pill__detail">{state.detail}</span>
                                </li>
                            ))}
                        </ul>
                    </section>

                    <section className="table-panel" aria-labelledby="observation-table-title">
                        <div className="table-panel__header">
                            <h2 id="observation-table-title" className="section-title">
                                Recent observations
                            </h2>
                            <p className="table-panel__meta">3 rows · sorted by most recent capture time</p>
                        </div>

                        <div className="table-wrapper" role="region" aria-label="Observation results">
                            <table className="observation-table">
                                <thead>
                                    <tr>
                                        <th scope="col">Observation</th>
                                        <th scope="col">Candidate</th>
                                        <th scope="col">Captured</th>
                                        <th scope="col">Region</th>
                                        <th scope="col">Visibility</th>
                                        <th scope="col">Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {observationRows.map((row, index) => (
                                        <tr key={row.id} className={index === 0 ? "is-selected" : undefined}>
                                            <th scope="row">{row.id}</th>
                                            <td>{row.species}</td>
                                            <td>{row.time}</td>
                                            <td>{row.region}</td>
                                            <td>{row.visibility}</td>
                                            <td>{row.status}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </section>
                </main>

                <aside className="inspector" aria-label="Observation inspector">
                    <section className="inspector__section" aria-labelledby="selection-title">
                        <p className="eyebrow">Selected observation</p>
                        <h2 id="selection-title" className="section-title">
                            OBS-0007
                        </h2>
                        <dl className="detail-list">
                            <div>
                                <dt>Review state</dt>
                                <dd>Pending expert confirmation</dd>
                            </div>
                            <div>
                                <dt>Masking</dt>
                                <dd>Coordinates rounded for public presentation</dd>
                            </div>
                            <div>
                                <dt>Audio confidence</dt>
                                <dd>0.81 candidate confidence</dd>
                            </div>
                            <div>
                                <dt>Permission</dt>
                                <dd>Exact location hidden for non-review roles</dd>
                            </div>
                        </dl>
                    </section>

                    <section className="inspector__section" aria-labelledby="next-action-title">
                        <h2 id="next-action-title" className="section-title">
                            Next actions
                        </h2>
                        <ul className="action-list">
                            <li>Confirm candidate species after waveform inspection.</li>
                            <li>Review whether the masking level should remain restricted.</li>
                            <li>Escalate if protected-species handling requires reviewer approval.</li>
                        </ul>
                    </section>
                </aside>
            </div>
        </div>
    );
}
