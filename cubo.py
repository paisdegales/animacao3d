import numpy as np
import matplotlib.pyplot as plt
from stl import mesh
from matplotlib import animation, rc
from mpl_toolkits.mplot3d import Axes3D, art3d  
from math import pi,cos,sin

''' 
    Dupla: Carlos Daniel Albertino Vieira (Eng.Comp.) e Érica Miranda Gonçalves (Eng.Ele.)
'''

""" FUNCOES COMPLEMENTARES """
def set_axes_equal(ax): 
    #Equalizar as escalas dos eixos 3D para preserver a forma geométrica dos
    #objetos. Necessário pois as funções disponíveis na biblioteca do matplotlib
    #são pensadas para planos 2D, não sendo funcionais para o 3D.

    #Input
    # ax: variavel que armazena eixos do espaço R3
    
    #'Pegando' limites dos eixos
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    # x,y,z_range = armazenam o alcance(modulo) do dominio de seus respectivos eixos
    # x,y,z_middle = armazenam a media dos valores pertencentes ao dominio de seus
    # respectivos eixos, com objetivo de identificar ponto médio desses. Como a 
    # media para eixos coordenados simetricos é 0, os 3 pontos medios consistem
    # nas coordenadas da origem do sistema

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # Os limites do plot podem ser interpretados como os de uma esfera,
    # por isso a metade do alcance dos eixos coordenados resulta no raio
    plot_radius = 0.5*max([x_range, y_range, z_range])

    # Definindo os extremos do intervalo de cada eixo coordenado do R3
    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

""" FUNCOES DE ROTAÇÃO E TRANSLAÇÃO NO EIXO Z, Y, X"""
''' Funcoes baseadas nos slides disponibilizados pela professora no classroom '''

def z_rotation(angle):
    rotation_matrix=np.array([[cos(angle),-sin(angle),0,0],[sin(angle),cos(angle),0,0],[0,0,1,0],[0,0,0,1]])
    return rotation_matrix
    
def y_rotation(angle):
    rotation_matrix=np.array([[cos(angle),0,sin(angle),0],[0,1,0,0],[-sin(angle),0,cos(angle),0],[0,0,0,1]])
    return rotation_matrix

def x_rotation(angle):
    rotation_matrix=np.array([[1,0,0,0],[0, cos(angle),-sin(angle),0],[0, sin(angle),cos(angle),0],[0,0,0,1]])
    return rotation_matrix

def move (dx,dy,dz):
    translation = np.array([dx,dy,dz,1])
    T_matrix = np.eye(4)
    T_matrix[:,-1] = translation.T
    return T_matrix

""" CARREGANDO ARQUIVO STL """

# Carregando o arquivo STL e adicionando os vetores a variavel your_mesh
your_mesh = mesh.Mesh.from_file('./sample_data/tetris.stl')


# Definindo escalas a serem utilizadas para diminuir o tamanho do objeto contido
# no arquivo STL
scale1 = 0.5
scale2 = 2

# Armazenando as coordenadas x,y,z contidas na variavel your_mesh que sao os ver
# tices dos triangulos que formam o objeto
x = scale1*your_mesh.x.flatten()
y = scale1*your_mesh.y.flatten()
z = scale1*your_mesh.z.flatten()

# Recebendo os vetores que definem os triangulos que formam o objeto 
tetris_vectors = scale1*your_mesh.vectors

# Criando a matriz de coordenadas homogeneas correspondentes ao objeto 3D 
tetris = np.array([x.T,y.T,z.T,np.ones(x.size)])

''' Entrando peças do tetris '''
#Entrando com numero de peças existentes na animacao
n = 5
#Criando coleção que conterá todas as peças de tetris do jogo
col = []          
#Preenchendo a coleção das peças com copias do objeto contido no arquivo stl    
for i in range(n):
  col.append(tetris)

''' Cadastrando as peças estáticas que aparecem no cenário (1 apenas) '''
#Definindo angulo inicial de rotação da peça
ang = 90
ang_rad = (ang/180)*np.pi
#Criando as matrizes de translação/rotação
T = move(0, 0, -15);
Tx = move(15, 0, 0)
R = z_rotation(ang_rad)
#Criando matriz resultante da composição das matrizes previamente feitas
M = np.dot(R, T)
M = np.dot(Tx, M)

#Transladando/rotacionando as peças que queremos (no caso, apenas uma)
col[0] = np.dot(M, col[0]) 

''' Criando novo plot '''
fig = plt.figure(1,figsize=[10,10])
axes0 = plt.axes(projection='3d')
axes0.set_xlabel('Eixo X')
axes0.set_ylabel('Eixo Y')
axes0.set_zlabel('Eixo Z')

plt.close()

''' Criando objetos do plot  '''
#Vetor com a posição inicial (origem do sistema) dos objetos presentes na animação
objcs = []
#Vetor com a posicao em constante transformação dos objetos durante a animacao
objcs2 = []
#Vetor que contem varias cores unicas para facilitar a diferenciação das peças
c = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

for i in range(n):
  obj1, = axes0.plot3D([], [], [], lw=2,color=c[i])         #Criando elemento único
  objcs.append(obj1)                                        #Adicionando esse elemento a lista de objetos

for i in range(n):
  obj2, = axes0.plot3D([], [], [],'--', lw=2)               #Criando elemento único 
  objcs2.append(obj2)                                       #Adicionando esse elemento a lista de objetos


''' FUNCOES DE ANIMAÇÃO 3D '''
# Definindo função de inicialização da animação
def init():
    # Preenchendo coleção dos objetos. Note que aqui é utilizado o vetor objcs,
    # que contem a posição inicial (origem) de cada objeto
    for i in range(n):                            
      objcs[i].set_data(col[i][0,:], col[i][1,:])
      objcs[i].set_3d_properties(col[i][2,:])

    # Utilizando a função definida anteriormente para acertar a escala dos eixos
    # do R3. A autoescala será feita sempre em relação ao último objeto a ser plotado,
    # o qual não sofrerá modificação por ser utilizado nessa parte do código
    axes0.auto_scale_xyz(scale2*col[n-1][0,:],scale2*col[n-1][1,:],scale2*col[n-1][2,:])
    set_axes_equal(axes0)

    # Retornando coleção preenchida dos objetos do cenário agora inicializados
    return (objcs)
    
# Função da animação, a qual é chamada sequenciamente.
def animate(i):
  # Primeiro if: Movimentação da peça laranja.
  # Movimentos realizados: Translação no eixo z.
  if i<51:
    T3 = move(0, 0, -0.3*i)
    tetris2 = np.dot(T3,col[1])
    objcs2[1].set_data(tetris2[0,:], tetris2[1,:])
    objcs2[1].set_3d_properties(tetris2[2,:])

  # Segundo if: Movimentação da peça verde
  # Movimentos realizados: Translação no eixo z e y, Rotação no eixo x
  if i>50 and i<102:
    T3 = move(0, 0.2*(i-51), -0.3*(i-51))
    #Angulo total da rotação: 90
    ang = (i-51)*1.8
    ang_rad = (ang/180)*np.pi
    R1 = x_rotation(ang_rad)
    M = np.dot(T3, R1)
    tetris2 = np.dot(M,col[2])
    objcs2[2].set_data(tetris2[0,:], tetris2[1,:])
    objcs2[2].set_3d_properties(tetris2[2,:])
    # Modificando ponto de vista para facilitar visualização dos movimentos e
    # do encaixa das peças
    axes0.view_init(elev=10., azim=3.6*(i-51))

  # Terceiro if: Movimentação da peça vermelha
  # Movimentos realizados: Rotação no eixo y e z
  if i>101 and i<152:
    #Angulo total da rotação: 90
    ang = (i-101)*1.8
    ang_rad = (ang/180)*np.pi
    R1 = z_rotation(ang_rad)
    R2 = y_rotation(-ang_rad)
    M = np.dot(R2, R1)
    tetris2 = np.dot(M,col[3])
    objcs2[3].set_data(tetris2[0,:], tetris2[1,:])
    objcs2[3].set_3d_properties(tetris2[2,:])
    # Modificando ponto de vista para facilitar visualização dos movimentos e
    # do encaixa das peças
    axes0.view_init(elev=10., azim=180-1.8*(i-101))

  # Quarto if: Movimentação da peça vermelha (continuação do movimento anterior)
  # Movimentos realizados: Translação no eixo z
  if i>151:
    T3 = move(0, 0, -0.2*(i-152))
    ang = 90
    ang_rad = (ang/180)*np.pi    
    R1 = z_rotation(ang_rad)
    R2 = y_rotation(-ang_rad)
    M = np.dot(R2, R1)
    M = np.dot(T3, M)
    tetris2 = np.dot(M,col[3])
    objcs2[3].set_data(tetris2[0,:], tetris2[1,:])
    objcs2[3].set_3d_properties(tetris2[2,:])
    # Modificando ponto de vista para facilitar visualização dos movimentos e
    # do encaixa das peças
    axes0.view_init(elev=10., azim=90+1.8*(i-152))

  # Corrigindo a escala do R3 para que o formato da figura seja preservado
  axes0.auto_scale_xyz(scale2*col[n-1][0,:],scale2*col[n-1][1,:],scale2*col[n-1][2,:])
  set_axes_equal(axes0)

  # Retornando coleção dos objetos 'transformados' da animação 
  return (objcs2)

''' ANIMATION '''

# Fazendo animação
anim = animation.FuncAnimation(fig, animate, init_func=init,
                             frames=200, interval=100, blit=True)

# Fazendo funcionar no google colab
rc('animation', html='jshtml')
anim

#Salvando arquivo em formato mp4
#f = r"./sample_data/animation.mp4" 
#writervideo = animation.FFMpegWriter(fps=60) 
#anim.save(f, writer=writervideo)
