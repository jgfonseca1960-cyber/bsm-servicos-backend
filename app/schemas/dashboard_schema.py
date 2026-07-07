from pydantic import BaseModel

class DashboardResumo(BaseModel):
    total_empresas: int
    total_servicos: int
    total_avaliacoes: int
    empresas_avaliadas: int
    empresas_sem_avaliacao: int
    media_geral: float