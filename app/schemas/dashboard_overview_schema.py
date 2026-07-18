from pydantic import BaseModel


class DashboardOverviewSchema(BaseModel):
    usuarios: int
    empresas: int
    servicos: int
    avaliacoes: int

    usuarios_ativos: int

    empresas_gratuitas: int
    empresas_premium: int
    empresas_master: int

    novas_empresas: int
    novos_usuarios: int

    avaliacoes_hoje: int
    avaliacoes_mes: int

    media_geral: float

    class Config:
        from_attributes = True