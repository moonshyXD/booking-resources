import './choose-organization.css'

const ChooseOrganization = () => {
    return(

        <div className="choose-organization">
            <div className="content-box">
                <h1 className="main-text"> ПЛАТФОРМА <br/> БРОНИРОВАНИЯ РЕСУРСОВ </h1>

                <label className="dropdown-label">
                    ВЫБЕРИТЕ ОРГАНИЗАЦИЮ
                </label>
                <div className="dropdown">
                    <button className="btn btn-secondary" style={{display: 'flex', alignItems: 'center', gap: '10px'}}
                            type="button" data-bs-toggle="dropdown">
                        <div className="label-secondary">наименование организации</div>
                        <i className="bi bi-chevron-compact-down" style={{color: 'red', fontSize: '24px'}}></i>
                    </button>
                    <ul className="dropdown-menu">
                        <li><a className="dropdown-item" href="#">T1</a></li>
                        <li><a className="dropdown-item" href="#">WB</a></li>
                    </ul>
                </div>
                <button type="button" className="btn button-to-entrance">BОЙТИ</button>
            </div>
        </div>

    )
}

export default ChooseOrganization;