def parse_uf(uf):
    
    UFS = {
        
        ('BR', 'BRASIL'): 'BR',
        
        # Região Norte
        ('AC', 'ACRE'): 'AC',
        ('AM', 'AMAZONAS'): 'AM',
        ('AP', 'AMAPA', 'AMAPÁ'): 'AP',
        ('PA', 'PARA', 'PARÁ'): 'PA',
        ('RO', 'RONDONIA', 'RONDÔNIA'): 'RO',
        ('RR', 'RORAIMA'): 'RR',
        ('TO', 'TOCANTINS'): 'TO',
        
        # Região Nordeste
        ('AL', 'ALAGOAS'): 'AL',
        ('BA', 'BAHIA'): 'BA',
        ('CE', 'CEARA', 'CEARÁ'): 'CE',
        ('MA', 'MARANHAO', 'MARANHÃO'): 'MA',
        ('PB', 'PARAIBA', 'PARAÍBA'): 'PB',
        ('PE', 'PERNAMBUCO'): 'PE',
        ('PI', 'PIAUI', 'PIAUÍ'): 'PI',
        ('RN', 'RIOGRANDEDONORTE'): 'RN',
        ('SE', 'SERGIPE'): 'SE',
        
        # Região Centro-Oeste
        ('DF', 'DISTRITOFEDERAL'): 'DF',
        ('GO', 'GOIAS', 'GOIÁS'): 'GO',
        ('MT', 'MATOGROSSO'): 'MT',
        ('MS', 'MATOGROSSODOSUL'): 'MS',
        
        # Região Sudeste
        ('ES', 'ESPIRITOSANTO', 'ESPÍRITOSANTO'): 'ES',
        ('MG', 'MINASGERAIS', 'MINAS'): 'MG',
        ('RJ', 'RIODEJANEIRO', 'RIO'): 'RJ',
        ('SP', 'SAOPAULO', 'SÃOPAULO'): 'SP',
        
        # Região Sul
        ('PR', 'PARANA', 'PARANÁ'): 'PR',
        ('RS', 'RIOGRANDEDOSUL'): 'RS',
        ('SC', 'SANTACATARINA'): 'SC',
    
    }
    
    mapping = {}
    for key in UFS:
        for value in key:
            mapping.update({value: UFS[key]})
    
    s = uf.upper().replace(' ', '')
    
    return mapping[s]