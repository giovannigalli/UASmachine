parser = ArgumentParser()
parser.add_argument('--mainPath', default=mainPath, help='Path to project root')  
parser.add_argument('--trial', default='dau.1', help='Trial name')
parser.add_argument('--id_crop', default='monkey.obj', help='Name of the crop object to be imported')
parser.add_argument('--id_gcp', default='gcp.obj', help='Name of the gcp object to be imported')
parser.add_argument('--pos_cam_z', default=20, help='Flight height')
parser.add_argument('--overlap', default=.8, help='Overlapping - front and side')
parser.add_argument('--camera', default='Phantom4', help='UAVs camera')
parser.add_argument('--spacing_row', default=.5, help='Spacing between rows')
parser.add_argument('--spacing_plant', default=.3, help='Spacing between plants')
parser.add_argument('--spacing_block', default=1, help='Spacing between blocks')
parser.add_argument('--soil', default=0, help='Soil altitude')
parser.add_argument('--layout', default=np.matrix([[-1,1],[0,1],[1,1],[-1,0],[0,0],[1,0],[-1,-1],[0,-1],[1,-1]]), help='The layout represents the blocks in the field. The [X,Y] represent relative positions on the Cartesian map; Blocks are layed out from left to right, top to bottom (but it can be changed); Use integer for odd; Use decimal for even; Block layout, default is 3x3; Other layouts: 2x2: layout = np.matrix([[-.5,.5],[.5,.5],[-.5,-.5],[.5,-.5]]); 2x1: layout = np.matrix([[-.5,0],[.5,0]])')
parser.add_argument('--layout_gcp', default=np.matrix([[-1.8,1.8],[1.8,1.8],[-1.8,-1.8],[1.8,-1.8]]), help='GCP layout has to be adjusted manually according to the blocking layout; Default is 4 on the sides')

par, _ = parser.parse_known_args()

#internal processing
info_par = np.loadtxt(par.mainPath + '/R/par.'+ par.trial + '.txt').tolist() #imports parameters
n_treat_byblock = int(info_par[5])
n_treat_row = int(info_par[4])
n_plant = int(info_par[2])
n_block = par.layout.shape[0]
blockX = n_plant * par.spacing_plant
blockY = n_treat_byblock * n_treat_row * par.spacing_row
n_row = n_treat_byblock * n_treat_row + 2 #added border
n_plant = n_plant + 2 #added border
Xcoord = par.layout[:,0] * (blockX + par.spacing_block)
Ycoord = par.layout[:,1] * (blockY + par.spacing_block)

#internal addition of arguments
parser.add_argument('--info_par', default=info_par, help='Internal processing')
parser.add_argument('--n_treat_byblock', default=n_treat_byblock, help='Internal processing')
parser.add_argument('--n_treat_row', default=n_treat_row, help='Internal processing')
parser.add_argument('--n_plant', default=n_plant, help='Internal processing')
parser.add_argument('--n_block', default=n_block, help='Internal processing')
parser.add_argument('--blockX', default=blockX, help='Internal processing')
parser.add_argument('--blockY', default=blockY, help='Internal processing')
parser.add_argument('--n_row', default=n_row, help='Internal processing')
parser.add_argument('--n_plant', default=n_plant, help='Internal processing')
parser.add_argument('--Xcoord', default=Xcoord, help='Internal processing')
parser.add_argument('--Ycoord', default=Ycoord, help='Internal processing')

par, _ = parser.parse_known_args()