import './choose-organization.css'
import { useQuery } from '@tanstack/react-query'
import { fetchOrganizations, selectOrganization } from '../../api/organizationsApi'
import type { Organization } from '../../types/organization'
import {useState} from "react";
import {useNavigate} from "react-router-dom";

const ChooseOrganization = () => {
    const {data: organizations, isLoading, error} = useQuery({
        queryKey: ['organizations'],
        queryFn: fetchOrganizations,
    })
    const [selectedOrg, setSelectedOrg] = useState<Organization | null>(null)
    const [searchQuery, setSearchQuery] = useState('')
    const [isOpen, setIsOpen] = useState(false)
    const [isSaving, setIsSaving] = useState(false)

    const handleSelect = (org: Organization) => {
        setSelectedOrg(org);
    }

    const navigate = useNavigate()
    const handleLogin = async () => {
        if(!selectedOrg) return

        setIsSaving(true)

        try{
            await selectOrganization(selectedOrg.id)
            navigate('/login')
        } catch(error){
            console.error('Ошибка: ', error)
        }finally {
            setIsSaving(false)
        }
    }

    if(isLoading) return <div className="default-text">Загрузка организаций...</div>
    if (error) return <div className="default-text"> Ошибка загрузки</div>
    if (organizations?.length === 0) return <div className="default-text">Организаций пока нет</div>

    return(
        <div className="choose-organization">
            <div className="content-box">
                <h1 className="main-text"> ПЛАТФОРМА <br/> БРОНИРОВАНИЯ РЕСУРСОВ </h1>

                <label className="dropdown-label">
                    ВЫБЕРИТЕ ОРГАНИЗАЦИЮ
                </label>

                {selectedOrg && selectedOrg.name.length > 0 ? <i className="bi bi-x-lg icons" onClick={(e) => {
                    e.preventDefault();      // отменяет действие по умолчанию
                    e.stopPropagation();     // останавливает всплытие
                    setSelectedOrg(null);
                }} style={{ cursor: 'pointer', marginLeft: 'auto' }}></i> : <i className="bi bi-chevron-down icons"></i>}

                <div className="dropdown">
                    <button className="btn btn-secondary" style={{display: 'flex', alignItems: 'center', gap: '10px'}}
                            type="button" data-bs-toggle="dropdown">
                        <div className="label-secondary">
                            {selectedOrg ? ( selectedOrg.name) : ( <div className="selected-label">наименование организации</div>)}
                        </div>
                    </button>

                    <ul className="dropdown-menu">
                        {organizations?.map((org: Organization) => (
                            <li key={org.id}>
                                <button className="dropdown-item" onClick={()=>handleSelect(org)} >{org.name}</button>
                            </li>
                        ))}
                    </ul>
                </div>
                <button type="button" className="btn button-to-entrance" disabled={!selectedOrg} onClick={handleLogin}> {isSaving ? 'Отправка...' : 'ВОЙТИ'}</button>
            </div>
        </div>

    )
}

export default ChooseOrganization;