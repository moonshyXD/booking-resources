import './choose-organization.css'
import { useDispatch, useSelector } from 'react-redux'
import { clearOrganization, setOrganization, setOrganizationError, setOrganizationLoading } from '../../store/organizationSlice'
import { useQuery } from '@tanstack/react-query'
import { fetchOrganizations } from '../../api/organizationsApi'
import type { Organization } from '../../types/organization'
import { useEffect, useState, type KeyboardEvent, type MouseEvent } from "react";
import {useNavigate} from "react-router-dom";
import ContentBox from '../../components/СontentBox/contentBox'
import Wrapper from '../../components/Wrapper/wrapper'
import type { RootState } from '../../store/store'


const ChooseOrganization = () => {
    const {data: organizations, isLoading, error} = useQuery({
        queryKey: ['organizations'],
        queryFn: fetchOrganizations,
    })

    const [selectedOrg, setSelectedOrg] = useState<Organization | null>(null)
    const [searchQuery, setSearchQuery] = useState('')
    const [isOpen, setIsOpen] = useState(false)
    const [isSaving, setIsSaving] = useState(false)
    const dispatch = useDispatch()
    const selectedOrgId = useSelector((state: RootState) => state.organization.selectedOrgId)

    const handleSelect = (org: Organization) => {
        setSelectedOrg(org);
        setSearchQuery('');
        dispatch(setOrganization(org))
        localStorage.setItem('organizationId', org.id)
        localStorage.setItem('organizationSlug', org.slug)
    }

    const navigate = useNavigate()
    const handleLogin = async () => {
        if(!selectedOrg) return

        setIsSaving(true)
        setSearchQuery('')


        try{
            navigate('/login')
        } catch(error){
            console.error('Ошибка: ', error)
        }finally {
            setIsSaving(false)
        }
    }

    const filteredOrganizations = organizations?.filter(org =>
        org.name.toLowerCase().includes(searchQuery.toLowerCase())
    ) || []

    useEffect(() => {
        if (!isOpen) {
            setSearchQuery('')
        }
    }, [isOpen])
    useEffect(() => {
        if (selectedOrgId && organizations) {
            const savedOrg = organizations.find(org => org.id === selectedOrgId)
            if (savedOrg) {
                setSelectedOrg(savedOrg)
                dispatch(setOrganization(savedOrg))
            }
        }
    }, [selectedOrgId, organizations, dispatch])

    useEffect(() => {
        dispatch(setOrganizationLoading(isLoading))
    }, [isLoading, dispatch])

    useEffect(() => {
        if (!error) {
            dispatch(setOrganizationError(null))
            return
        }

        const message = error instanceof Error ? error.message : 'Ошибка загрузки организаций'
        dispatch(setOrganizationError(message))
    }, [error, dispatch])

    if(isLoading) return (
        <Wrapper>
            <div className="choose-organization-page">
                <div className="default-text">Загрузка организаций...</div>
            </div>
        </Wrapper>
    )
    if (error) return (
        <Wrapper>
            <div className="choose-organization-page">
                <div className="default-text"> Ошибка загрузки</div>
            </div>
        </Wrapper>
    )

    return(
        <Wrapper>
            <div
                className="choose-organization-page"
                tabIndex={0}
                onKeyDown={(e: KeyboardEvent<HTMLDivElement>) => {
                 const key = e.key
                 if (key.length === 1 && !e.ctrlKey && !e.altKey) {
                     setSearchQuery(prev => prev + key)
                 } else if (key === 'Backspace') {
                     setSearchQuery(prev => prev.slice(0, -1))
                 } else if (key === 'Escape') {
                     setSearchQuery('')
                 }
             }}
            >
            <ContentBox>
                <h1 className="main-text"> ПЛАТФОРМА <br/> БРОНИРОВАНИЯ РЕСУРСОВ </h1>

                <label className="dropdown-label">
                    ВЫБЕРИТЕ ОРГАНИЗАЦИЮ
                </label>

                <div className="dropdown">
                    <button
                        className="btn btn-secondary choose-org-dropdown-btn"
                        type="button"
                        data-bs-toggle="dropdown"
                        onClick={() => setIsOpen(!isOpen)}
                    >
                        <div className="label-secondary">
                            {selectedOrg ? selectedOrg.name : <div className="selected-label">наименование организации</div>}
                        </div>
                        {selectedOrg && selectedOrg.name.length > 0 ? (
                            <i
                                className="bi bi-x-lg choose-org-icon"
                                onClick={(e: MouseEvent<HTMLElement>) => {
                                    e.preventDefault();
                                    e.stopPropagation();
                                    setSelectedOrg(null);
                                    dispatch(clearOrganization())
                                    localStorage.removeItem('organizationId')
                                    localStorage.removeItem('organizationSlug')
                                }}
                                role="button"
                                aria-label="Сбросить выбор"
                            />
                        ) : (
                            <i className="bi bi-chevron-down choose-org-icon" aria-hidden />
                        )}
                    </button>
                    <ul className="dropdown-menu">
                        {filteredOrganizations?.length === 0 ? (
                            <li>
                                <div className="dropdown-item no-org">
                                    Организаций нет
                                </div>
                            </li>
                        ) : (
                            filteredOrganizations?.map((org: Organization) => (
                                <li key={org.id}>
                                    <button className="dropdown-item" onClick={() => handleSelect(org)}>
                                        {org.name}
                                    </button>
                                </li>
                            ))
                        )}
                    </ul>
                </div>
                <button type="button" className="btn button-to-entrance" disabled={!selectedOrg} onClick={handleLogin} > {isSaving ? 'Отправка...' : 'ВОЙТИ'}</button>
            </ContentBox>
            </div>
        </Wrapper>

    )
}

export default ChooseOrganization;