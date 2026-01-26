# Pontu - Plataforma de Turismo Sustentável

![Status](https://img.shields.io/badge/status-ativo-brightgreen)
![Linguagem](https://img.shields.io/badge/linguagem-HTML%2FCSS%2FJavaScript-blue)
![Licença](https://img.shields.io/badge/licença-MIT-green)

## 📋 Descrição

**Pontu** é uma plataforma inovadora de transporte sustentável que conecta passageiros conscientes com roteiros de viagem personalizados, promovendo a exploração responsável de destinos, muitas vezes escapando do trânsito e ajudando outros passageiros que pretendem utilizar o mesmo tranporte. A aplicação visa transformar a forma como as pessoas planejam e realizam viagens, integrando práticas sustentáveis e socialmente responsáveis na indústria do turismo.

---

## 🎯 Utilidade para a Sociedade

### Impacto Social e Ambiental

Pontu atua como facilitadora na democratização do transporte consciente, permitindo que passageiros de transporte público:

- **Encontrem as melhores rotas** com informações sobre transporte público, bicicletas e mobilidade ativa
- **Otimizem seus deslocamentos** reduzindo tempo de viagem e emissões de carbono
- **Reduzam a pegada de carbono** escolhendo alternativas sustentáveis ao transporte individual
- **Contribuam para cidades mais limpas** usando transporte coletivo e compartilhado
- **Compartilhem experiências** e dicas com a comunidade de passageiros conscientes

### ODS (Objetivos de Desenvolvimento Sustentável)

Pontu está alinhado com os seguintes ODS da ONU focando em **transporte consciente e sustentável**:

| ODS | Alinhamento | Ação |
|-----|-----------|------|
| **ODS 7** - Energia Limpa e Acessível | Promove transporte com fontes de energia renovável | Incentiva uso de bicicletas, transportes elétricos e a pé em viagens |
| **ODS 11** - Cidades e Comunidades Sustentáveis | Desenvolve mobilidade urbana consciente | Rotas que priorizam transporte público, compartilhado e não poluente |
| **ODS 12** - Consumo e Produção Responsáveis | Reduz consumo desnecessário de combustível | Planejamento eficiente de rotas com menor consumo energético |
| **ODS 13** - Ação Climática | Diminui emissões de carbono no setor de transporte | Cálculo e compensação de pegada de carbono em viagens |
| **ODS 15** - Vida Terrestre | Protege ecossistemas de impactos da mobilidade | Roteiros que evitam áreas sensíveis e preservam biodiversidade |
| **ODS 17** - Parcerias para os Objetivos | Conecta viajantes, comunidades e operadores sustentáveis | Rede colaborativa para expansão de transporte consciente |

---

## 🌍 Cobertura Geográfica

Pontu foi desenvolvido com foco inicial em **mobilidade urbana sustentável em cidades brasileiras**, com planos de expansão:

- **Brasil**: Cidades com sistemas de transporte público em desenvolvimento
- **Metropolitanas**: Foco em grandes centros urbanos e regiões metropolitanas
- **Expansão Global**: Integração com sistemas de transporte público de outras cidades

---

## 💻 Ferramentas e Tecnologias

### Stack Tecnológico Atual (HTML/CSS/JavaScript)

| Categoria | Ferramenta | Versão |
|-----------|-----------|--------|
| **Frontend** | HTML5, CSS3, JavaScript (ES6+) | - |
| **Estilização** | CSS Responsivo | - |
| **Hospedagem** | GitHub Pages | - |
| **Versionamento** | Git & GitHub | - |

### Stack Original (Descontinuado)

O projeto foi **inicialmente desenvolvido em Python com Flask** e banco de dados **SQLite**, permitindo funcionalidades mais avançadas:

```python
# Stack original:
- Backend: Python 3.x + Flask
- Banco de Dados: SQLite
- Frontend: Templates Jinja2
- Autenticação: Flask-Login
- ORM: SQLAlchemy
```

---

## 📱 Funcionalidades Principais

### 1. **Login e Autenticação**
- Acesso seguro para usuários cadastrados
- Recuperação de senha
- Opção de visualização sem login

### 2. **Explorar Rotas de Transporte**
- Catálogo de rotas de transporte público disponíveis
- Filtros por tipo de transporte, tempo de deslocamento e emissões de carbono
- Avaliações de passageiros sobre qualidade do serviço
- Informações sobre operadoras sustentáveis e transporte elétrico

### 3. **Planejar Viajem**
- Planejador interativo de rotas combinando diferentes meios de transporte
- Sugestões automáticas baseadas em preferências de sustentabilidade
- Cálculo de pegada de carbono economizada ao usar transporte público
- Comparação entre transporte individual vs. transporte público

### 4. **Histórico de Viajem**
- Registro de trajetos realizados usando transporte público
- Estatísticas de impacto (CO2 economizado, economia de combustível, etc.)
- Compartilhamento de experiências com a comunidade

### 5. **Favoritos**
- Salvamento de rotas de transporte frequentes
- Lista personalizada de trajetos preferidos

### 6. **Perfil do Usuário**
- Gerenciamento de informações pessoais
- Preferências de transporte e mobilidade
- Estatísticas de sustentabilidade e impacto ambiental

### 7. **Cadastro de Rotas**
- Ferramenta para usuários e operadoras criarem novas rotas de transporte
- Upload de informações sobre práticas sustentáveis das operadoras

### 8. **Resgate de Certificados**
- Sistema de gamificação com certificados de passageiro consciente
- Badges de realização e metas de sustentabilidade
- Pontuação de impacto ambiental positivo

### 9. **Feedback e Avaliações**
- Sistema de comentários e ratings
- Sugestões de melhorias

---

## 🔄 Evolução do Projeto: Python/Flask → HTML/CSS/JavaScript

### Por que a Mudança?

**Contexto Acadêmico:**
O projeto foi originalmente concebido em **Python com Flask e SQLite** para máxima funcionalidade backend. No entanto, devido a **requisitos específicos do projeto acadêmico**, foi necessário realizar uma **migração estratégica para HTML/CSS/JavaScript puro**.

### Motivos da Reprogramação

```
DESAFIO ORIGINAL:
├── Python/Flask com banco de dados SQLite
├── Aplicação rodando localmente
├── Limitações de deploy (server necessário)
└── Impossibilidade de entrega em tempo hábil com hosting disponível

SOLUÇÃO IMPLEMENTADA:
├── Migração para HTML5/CSS3/JavaScript
├── Deploy via GitHub Pages (sem necessidade de servidor backend)
├── Mantém funcionalidades principais com localStorage
└── Implementação bem-sucedida e entrega no prazo
```

### Impacto da Mudança

| Aspecto | Python/Flask | HTML/CSS/JS |
|--------|--------------|------------|
| **Backend** | Sim (Flask) | Não (Frontend-only) |
| **Banco de Dados** | SQLite (Local) | localStorage (Browser) |
| **Deploy** | Servidor necessário | GitHub Pages (Gratuito) |
| **Tempo de desenvolvimento** | Mais longo | Mais rápido |
| **Funcionalidades** | Mais avançadas | Essenciais implementadas |
| **Acesso** | Requer hosting pago | URL direta |

### Lições Aprendidas

✅ A refatoração foi bem-sucedida na implementação das funcionalidades críticas
✅ GitHub Pages oferece solução viável para projetos acadêmicos
✅ Frontend moderno consegue simular muitas funcionalidades backend com localStorage
⚠️ Sem backend, algumas funcionalidades (busca avançada, notificações em tempo real, persistência de dados entre dispositivos) ficaram limitadas

---

## 🚀 Como Usar

### Acesso Online
Acesse diretamente via GitHub Pages: [Pontu - Plataforma de Transporte Sustentável](https://leomoreeiraa.github.io/Pontu/index.html)

### Desenvolvimento Local

1. **Clone o repositório:**
```bash
git clone https://github.com/LeoMoreeiraa/Pontu.git
cd Pontu
```

2. **Abra no navegador:**
```bash
# Opção 1: Abrir arquivo diretamente
open index.html

# Opção 2: Usar servidor local Python
python3 -m http.server 8000
# Acesse: http://localhost:8000
```

---

## 📁 Estrutura do Projeto

```
Pontu/
├── index.html                 # Página de splash/login
├── home.html                  # Página principal
├── explorar.html              # Exploração de rotas de transporte
├── planejar.html              # Planejador de deslocamentos
├── historico.html             # Histórico de deslocamentos
├── favoritos.html             # Rotas favoritas
├── perfil.html                # Perfil do usuário
├── cadastro.html              # Cadastro de novo usuário
├── rotas.html                 # Gestão de rotas
├── registrar_viagem.html      # Registro de deslocamento realizado
├── resgatar.html              # Resgate de certificados
├── feedback.html              # Sistema de feedback
├── static/
│   ├── style.css              # Estilos globais
│   ├── css/
│   │   └── base.css           # Base CSS
│   └── images/                # Imagens do projeto
└── README.md                  # Documentação (este arquivo)
```

---

## 🛠️ Especificações Técnicas

### Frontend
- **Linguagem:** HTML5, CSS3, JavaScript (ES6+)
- **Design:** Responsivo (Mobile-first)
- **Paleta de Cores:** Verdes sustentáveis (#4CAF50, #81C784)
- **Tipografia:** Poppins (moderna e legível)
- **Armazenamento:** localStorage para persistência de dados

### Performance
- ✅ Carregamento rápido (estático)
- ✅ Sem requisições de servidor
- ✅ Funciona offline (após primeiro carregamento)
- ✅ Otimizado para mobile

### Compatibilidade
- ✅ Chrome, Firefox, Safari, Edge (últimas 2 versões)
- ✅ Mobile (iOS Safari, Chrome Mobile)
- ✅ Tablets

---

## 📊 Dados e Armazenamento

### Dados Armazenados Localmente (localStorage)
- Perfil do usuário
- Deslocamentos planejados
- Rotas favoritas
- Histórico de deslocamentos
- Certificados ganhos

**⚠️ Nota:** Dados são armazenados apenas no navegador local. Ao limpar cache/cookies, dados podem ser perdidos.

---

## 🎓 Contexto Acadêmico

Este projeto foi desenvolvido como trabalho acadêmico com os seguintes objetivos de aprendizado:

✅ Desenvolvimento full-stack (Python/Flask)
✅ Design de interface responsiva
✅ Gestão de projeto e versionamento Git
✅ Integração com objetivos de desenvolvimento sustentável
✅ Pensamento crítico sobre impacto social e ambiental
✅ Adaptação de soluções técnicas conforme requisitos mudam

---

## 📈 Roadmap Futuro

- [ ] Implementar backend em Node.js/Express para funcionalidades avançadas
- [ ] Banco de dados em PostgreSQL para persistência multi-usuário
- [ ] API de geolocalização para rotas baseadas em localização em tempo real
- [ ] Integração com APIs de operadoras de transporte público
- [ ] Sistema de notificações em tempo real sobre atrasos e alterações
- [ ] Aplicativo mobile (React Native/Flutter)
- [ ] Parcerias com operadores de transporte público sustentável

---

## 📝 Licença

Este projeto está licenciado sob a licença **MIT** - veja o arquivo LICENSE para detalhes.

---

## 👥 Contribuições

Contribuições são bem-vindas! Se você tem sugestões ou quer melhorar o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📧 Contato

Para dúvidas, sugestões ou parcerias relacionadas ao projeto:

**Desenvolvedor:** Leonardo Moreira  
**GitHub:** [@LeoMoreeiraa](https://github.com/LeoMoreeiraa)  
**Email:** [leonardomsantos12@gmail.com]

---

## 🌱 Comprometimento com Sustentabilidade

> *"Deslocar-se conscientemente é investir no futuro do planeta."*

Pontu não é apenas uma plataforma; é um movimento pela mudança do paradigma de mobilidade urbana em nossas cidades. Cada deslocamento planejado através de Pontu representa um compromisso com a sustentabilidade, redução de emissões e melhoria da qualidade de vida urbana.

---

**Última atualização:** Janeiro de 2026
**Versão:** 1.0 (HTML/CSS/JavaScript)
