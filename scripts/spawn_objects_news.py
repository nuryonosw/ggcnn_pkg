#!/usr/bin/env python3

import rospy
import os
import rospkg
from gazebo_msgs.srv import SpawnModel, DeleteModel
from geometry_msgs.msg import Pose, Point, Quaternion
from tf.transformations import quaternion_from_euler
from std_srvs.srv import Empty  # Necessário para o unpause

def spawn_objects():
    rospy.init_node('spawn_objects_in_gazebo', anonymous=True)
    
    rospy.wait_for_service('/gazebo/spawn_sdf_model')
    spawn_model_prox = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)

    rospy.wait_for_service('/gazebo/delete_model')
    delete_model_prox = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)

    rospy.wait_for_service('/gazebo/unpause_physics')
    unpause_physics_prox = rospy.ServiceProxy('/gazebo/unpause_physics', Empty)

    rospack = rospkg.RosPack()
    try:
        ggcnn_pkg_path = rospack.get_path('ggcnn_pkg')
    except rospkg.ResourceNotFound:
        rospy.logerr("Pacote 'ggcnn_pkg' não encontrado. Verifique seu workspace.")
        return

    Z_SPAWN = 0.873  # Altura de spawn para os objetos (ajuste conforme necessário) 

    objects = [
        {"name": "003_cracker_box", "file": "models/objects_gazebo/ycb/003_cracker_box/003_cracker_box.sdf",
         "pos": [-0.50, 0.050, Z_SPAWN], "ori": [0.0, 0.0, 0.0]},
         
        {"name": "002_master_chef_can", "file": "models/objects_gazebo/ycb/002_master_chef_can/002_master_chef_can.sdf",
         "pos": [-0.45, -0.160, Z_SPAWN+0.06], "ori": [0.0, 0.0, 0.0]},
         
        {"name": "004_sugar_box", "file": "models/objects_gazebo/ycb/004_sugar_box/004_sugar_box.sdf",
         "pos": [-0.660629,-0.294873, Z_SPAWN], "ori": [0.0, 0.0, 0.0]},

        {"name": "008_pudding_box", "file": "models/objects_gazebo/ycb/008_pudding_box/008_pudding_box.sdf",
         "pos": [-0.736707, -0.061147, Z_SPAWN], "ori": [0.0, 0.0, 0.0]},

        {"name": "010_potted_meat_can", "file": "models/objects_gazebo/ycb/010_potted_meat_can/010_potted_meat_can.sdf",
         "pos": [-0.379882, 0.281240, Z_SPAWN], "ori": [0.0, 0.0, 0.0]},

        {"name": "077_rubiks_cube", "file": "models/objects_gazebo/ycb/077_rubiks_cube/077_rubiks_cube.sdf",
         "pos": [-0.687604, 0.246384, Z_SPAWN], "ori": [0.0, 0.0, 0.0]},

        {"name": "basket", "file": "models/objects_gazebo/basket/basket.sdf",
         "pos": [-0.974857, -0.009536, Z_SPAWN], "ori": [0.0, 0.0, 0.0]}
    ]

    rospy.loginfo("Deletando modelos antigos (Limpando a mesa)...")
    for obj in objects:
        try:
            delete_model_prox(obj["name"])
        except rospy.ServiceException:
            pass 

    rospy.sleep(1.0) 

    rospy.loginfo("Iniciando o Spawn dos modelos...")
    for obj in objects:
        model_path = os.path.join(ggcnn_pkg_path, obj["file"])
        
        if not os.path.exists(model_path):
            rospy.logerr(f"Arquivo não encontrado: {model_path}")
            continue

        with open(model_path, 'r') as f:
            model_xml = f.read()

        # =========================================================
        # HOTFIX: Conversão Dinâmica de URI (Evita travamento do Gazebo)
        # =========================================================
        model_dir_absolute = os.path.dirname(model_path)
        folder_name = os.path.basename(model_dir_absolute)
        
        # Substitui a tag nativa pela URI absoluta do seu computador
        model_xml = model_xml.replace(f"model://{folder_name}", f"file://{model_dir_absolute}")
        # =========================================================

        p = obj["pos"]
        e = obj["ori"]

        quat = quaternion_from_euler(e[0], e[1], e[2])

        initial_pose = Pose()
        initial_pose.position = Point(p[0], p[1], p[2])
        initial_pose.orientation = Quaternion(quat[0], quat[1], quat[2], quat[3])

        try:
            resp = spawn_model_prox(obj["name"], model_xml, "", initial_pose, "world")
            if resp.success:
                rospy.loginfo(f"Sucesso: {obj['name']} inserido.")
            else:
                rospy.logwarn(f"Falha ao inserir {obj['name']}: {resp.status_message}")
        except rospy.ServiceException as e:
            rospy.logerr(f"Erro na chamada do serviço: {e}")

        rospy.sleep(0.2) 

    rospy.loginfo("Despausando a física do Gazebo...")
    try:
        unpause_physics_prox()
    except rospy.ServiceException as e:
        rospy.logwarn("Não foi possível despausar a física.")

    rospy.loginfo("Cenário montado com sucesso!")

if __name__ == '__main__':
    try:
        spawn_objects()
    except rospy.ROSInterruptException:
        pass









# #!/usr/bin/env python3

# import rospy
# import os
# from gazebo_msgs.srv import SpawnModel, DeleteModel
# from geometry_msgs.msg import Pose, Point, Quaternion
# from tf.transformations import quaternion_from_euler  # Importa conversão

# def spawn_objects():
#     rospy.init_node('spawn_objects_in_gazebo', anonymous=True)
    
#     rospy.wait_for_service('/gazebo/spawn_sdf_model')
#     spawn_model_prox = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)

#     rospy.wait_for_service('/gazebo/delete_model')
#     delete_model_prox = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)

#     ggcnn_pkg_path = '/home/miguel/miguel_ws/src/ggcnn_pkg'

#     # Define positions and orientations for the objects
#     pos_bico_dosador = [-0.5, 0.05, 0.872]    #-0.05, -0.5, 0.872
#     ori_bico_dosador = [0.0, 0.0, 0.0]

#     pos_part1 = [-0.47, 0.09, 0.872]   #-0.09, -0.47, 0.872
#     ori_part1 = [0.0, 0.0, 0.0]

#     pos_part2 = [-0.46, 0.043, 0.872]   #-0.043, -0.46, 0.872
#     ori_part2 = [0.0, 0.0, 0.0]

#     pos_unob_1 = [-0.41, 0.058, 0.872]   #-0.058, -0.41, 0.872
#     ori_unob_1 = [0.0, 0.0, 0.0]    

#     pos_unob_2 = [-0.41, 0.13, 0.872]    #-0.13, -0.41, 0.872
#     ori_unob_2 = [0.0, 0.0, 0.0] 

#     pos_unob_3 = [-0.45, 0.141, 0.872]   #-0.141, -0.45, 0.872
#     ori_unob_3 = [0.0, 0.0, -1.57]   

#     pos_little_bin_box = [-0.45, -0.16, 0.872]    #0.16, -0.45, 0.872
#     ori_little_bin_box = [0.0, 0.0, 0.0]


#     objects_to_spawn_delete = [
#         {"name": "bico_dosador", "file": "models/bico_dosador/model.sdf",
#          "pos": {"x": pos_bico_dosador[0], "y": pos_bico_dosador[1], "z": pos_bico_dosador[2]},
#          "ori": {"roll": ori_bico_dosador[0], "pitch": ori_bico_dosador[1], "yaw": ori_bico_dosador[2]}},

#         {"name": "part1", "file": "models/part1/model.sdf",
#          "pos": {"x": pos_part1[0], "y": pos_part1[1], "z": pos_part1[2]},
#          "ori": {"roll": ori_part1[0], "pitch": ori_part1[1], "yaw": ori_part1[2]}},

#         {"name": "part2", "file": "models/part2/model.sdf",
#          "pos": {"x":  pos_part2[0], "y": pos_part2[1], "z": pos_part2[2]},
#          "ori": {"roll": ori_part2[0], "pitch": ori_part2[1], "yaw": ori_part2[2]}},

#         {"name": "unob_1", "file": "models/unob_1/model.sdf",
#          "pos": {"x": pos_unob_1[0], "y": pos_unob_1[1], "z": pos_unob_1[2]},
#          "ori": {"roll": ori_unob_1[0], "pitch": ori_unob_1[1], "yaw": ori_unob_1[2]}},

#         {"name": "unob_2", "file": "models/unob_2/model.sdf",
#          "pos": {"x": pos_unob_2[0], "y": pos_unob_2[1], "z": pos_unob_2[2]},
#          "ori": {"roll": ori_unob_2[0], "pitch": ori_unob_2[1], "yaw": ori_unob_2[2]}},

#         {"name": "unob_3", "file": "models/unob_3/model.sdf",
#          "pos": {"x": pos_unob_3[0], "y": pos_unob_3[1], "z": pos_unob_3[2]},
#          "ori": {"roll": ori_unob_3[0], "pitch": ori_unob_3[1], "yaw": ori_unob_3[2]}},

#         {"name": "little_bin_box", "file": "models/little_bin_box/model.sdf",
#          "pos": {"x": pos_little_bin_box[0], "y": pos_little_bin_box[1], "z": pos_little_bin_box[2]},
#          "ori": {"roll": ori_little_bin_box[0], "pitch": ori_little_bin_box[1], "yaw": ori_little_bin_box[2]}},
#     ]

#     objects_to_spawn = [
#         {"name": "bico_dosador", "file": "models/bico_dosador/model.sdf",
#          "pos": {"x": pos_bico_dosador[0], "y": pos_bico_dosador[1], "z": pos_bico_dosador[2]},
#          "ori": {"roll": ori_bico_dosador[0], "pitch": ori_bico_dosador[1], "yaw": ori_bico_dosador[2]}},

#         {"name": "part1", "file": "models/part1/model.sdf",
#          "pos": {"x": pos_part1[0], "y": pos_part1[1], "z": pos_part1[2]},
#          "ori": {"roll": ori_part1[0], "pitch": ori_part1[1], "yaw": ori_part1[2]}},

#         {"name": "part2", "file": "models/part2/model.sdf",
#          "pos": {"x":  pos_part2[0], "y": pos_part2[1], "z": pos_part2[2]},
#          "ori": {"roll": ori_part2[0], "pitch": ori_part2[1], "yaw": ori_part2[2]}},

#         {"name": "unob_1", "file": "models/unob_1/model.sdf",
#          "pos": {"x": pos_unob_1[0], "y": pos_unob_1[1], "z": pos_unob_1[2]},
#          "ori": {"roll": ori_unob_1[0], "pitch": ori_unob_1[1], "yaw": ori_unob_1[2]}},

#         {"name": "unob_2", "file": "models/unob_2/model.sdf",
#          "pos": {"x": pos_unob_2[0], "y": pos_unob_2[1], "z": pos_unob_2[2]},
#          "ori": {"roll": ori_unob_2[0], "pitch": ori_unob_2[1], "yaw": ori_unob_2[2]}},

#         {"name": "unob_3", "file": "models/unob_3/model.sdf",
#          "pos": {"x": pos_unob_3[0], "y": pos_unob_3[1], "z": pos_unob_3[2]},
#          "ori": {"roll": ori_unob_3[0], "pitch": ori_unob_3[1], "yaw": ori_unob_3[2]}},

#         {"name": "little_bin_box", "file": "models/little_bin_box/model.sdf",
#          "pos": {"x": pos_little_bin_box[0], "y": pos_little_bin_box[1], "z": pos_little_bin_box[2]},
#          "ori": {"roll": ori_little_bin_box[0], "pitch": ori_little_bin_box[1], "yaw": ori_little_bin_box[2]}},
#     ]

#     rospy.loginfo("Attempting to delete existing models...")
#     for obj in objects_to_spawn_delete:
#         try:
#             resp = delete_model_prox(obj["name"])
#             if resp.success:
#                 rospy.loginfo(f"Successfully deleted existing {obj['name']}")
#             else:
#                 rospy.logdebug(f"Could not delete {obj['name']} (might not exist): {resp.status_message}")
#         except rospy.ServiceException as e:
#             rospy.logerr(f"Delete service call failed for {obj['name']}: {e}")

#     rospy.sleep(0.5)

#     rospy.loginfo("Attempting to spawn models...")
#     for obj in objects_to_spawn:
#         model_path = os.path.join(ggcnn_pkg_path, obj["file"])
#         rospy.loginfo(f"Loading model from: {model_path}")
        
#         if not os.path.exists(model_path):
#             rospy.logerr(f"Model file not found: {model_path}")
#             continue

#         with open(model_path, 'r') as f:
#             model_xml = f.read()

#         p = obj["pos"]
#         e = obj["ori"]

#         # Converte Euler (roll, pitch, yaw) para quaternion
#         quat = quaternion_from_euler(e["roll"], e["pitch"], e["yaw"])

#         initial_pose = Pose()
#         initial_pose.position = Point(p["x"], p["y"], p["z"])
#         initial_pose.orientation = Quaternion(quat[0], quat[1], quat[2], quat[3])

#         rospy.loginfo(f"Spawning {obj['name']} from {model_path} at position {p} and Euler orientation {e}")
#         try:
#             resp = spawn_model_prox(obj["name"], model_xml, "", initial_pose, "world")
#             if resp.success:
#                 rospy.loginfo(f"Successfully spawned {obj['name']}")
#             else:
#                 rospy.logwarn(f"Failed to spawn {obj['name']}: {resp.status_message}")
#         except rospy.ServiceException as e:
#             rospy.logerr(f"Spawn service call failed: {e}")

#     rospy.loginfo("Finished attempting to spawn all objects.")

# if __name__ == '__main__':
#     try:
#         spawn_objects()
#     except rospy.ROSInterruptException:
#         pass



















# #!/usr/bin/env python3
# import rospy
# import tf
# import rospkg
# from gazebo_msgs.srv import SpawnModel, GetModelState, GetLinkState
# import time
# from geometry_msgs.msg import *
# from gazebo_msgs.msg import ModelState, ModelStates
# import os
# from os.path import expanduser
# from pathlib import Path
# from tf import TransformListener
# from tf.transformations import quaternion_from_euler

# class Moving():
# 	def __init__(self, model_name, Spawning1, y_pose, x_pose, z_pose, oriFinal, path):
# 		self.pub_model = rospy.Publisher('gazebo/set_model_state', ModelState, queue_size=1)
# 		self.model_name = model_name
# 		self.rate = rospy.Rate(10)
# 		self.path = path
# 		self.x_model_pose = x_pose
# 		self.y_model_pose = y_pose
# 		self.z_model_pose = z_pose
# 		self.Spawning1 = Spawning1
# 		self.orientation = oriFinal

# 	def spawning(self,):
# 		with open(self.path) as f:
# 			product_xml = f.read()
# 		item_name = "product_{0}_0".format(0)
# 		print("Spawning model:%s", self.model_name)
# 		# X and Y positions are somewhat in an incorrect order in Gazebo
# 		item_pose = Pose(Point(x=self.y_model_pose, y=self.x_model_pose,z=self.z_model_pose),
# 						 Quaternion(self.orientation[0], self.orientation[1], self.orientation[2], self.orientation[3]))
# 		self.Spawning1(self.model_name, product_xml, "", item_pose, "world")

# def uncluttered_objects():
# 	rospack = rospkg.RosPack()
# 	rospy.init_node('spawn_model')
# 	Spawning1 = rospy.ServiceProxy("gazebo/spawn_sdf_model", SpawnModel)
# 	rospy.wait_for_service("gazebo/spawn_sdf_model")
# 	model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
	
# 	Home = rospack.get_path('ggcnn_pkg')

# 	bico_dosador = Home + '/models/bico_dosador/model.sdf'
# 	little_bin_box = Home + '/models/little_bin_box/model.sdf'
# 	part1 = Home + '/models/part1/model.sdf'
# 	part2 = Home + '/models/part2/model.sdf'
# 	unob_1 = Home + '/models/unob_1/model.sdf'
# 	unob_2 = Home + '/models/unob_2/model.sdf'
# 	unob_3 = Home + '/models/unob_3/model.sdf'

# 	# The spawn need some time to wait the UR5 to show in Gazebo
# 	object_coordinates = model_coordinates("robot", "")
# 	z_position = object_coordinates.pose.position.z
# 	y_position = object_coordinates.pose.position.y
# 	x_position = object_coordinates.pose.position.x

# 	ptFinal = [-0.09, -0.47, -0.004] # all together in the bin
# 	oriFinal = quaternion_from_euler(0.0, 0.0, 0.0)
# 	moving4 = Moving("part1", Spawning1, x_position + ptFinal[0], y_position + ptFinal[1], z_position + ptFinal[2], oriFinal, part1)
# 	moving4.spawning()    

# 	ptFinal = [-0.043, -0.46, -0.002] # all together in the bin
# 	oriFinal = quaternion_from_euler(0.0, 0.0, -1.57)
# 	moving4 = Moving("part2", Spawning1, x_position + ptFinal[0], y_position + ptFinal[1], z_position + ptFinal[2], oriFinal, part2)
# 	moving4.spawning()

# 	ptFinal = [-0.05, -0.5, -0.005] # all together in the bin
# 	oriFinal = quaternion_from_euler(0.0, 0.0, 0.0)
# 	moving4 = Moving("bico_dosador", Spawning1, x_position + ptFinal[0], y_position + ptFinal[1], z_position + ptFinal[2], oriFinal, bico_dosador)
# 	moving4.spawning()

# 	ptFinal = [0.16, -0.45, 0.0] # all together in the bin
# 	oriFinal = quaternion_from_euler(0.0, 0.0, 0.0)
# 	moving4 = Moving("little_bin_box", Spawning1, x_position + ptFinal[0], y_position + ptFinal[1], z_position + ptFinal[2], oriFinal, little_bin_box)
# 	moving4.spawning()

# 	ptFinal = [-0.058, -0.41, -0.001] # all together in the bin
# 	oriFinal = quaternion_from_euler(0.0, 0.0, 0.0)
# 	moving4 = Moving("unob_1", Spawning1, x_position + ptFinal[0], y_position + ptFinal[1], z_position + ptFinal[2], oriFinal, unob_1)
# 	moving4.spawning()

# 	ptFinal = [-0.13, -0.41, -0.002] # all together in the bin
# 	oriFinal = quaternion_from_euler(0.0, 0.0, 0.0)
# 	moving4 = Moving("unob_2", Spawning1, x_position + ptFinal[0], y_position + ptFinal[1], z_position + ptFinal[2], oriFinal, unob_2)
# 	moving4.spawning()

# 	ptFinal = [-0.141, -0.45, -0.002] # all together in the bin
# 	oriFinal = quaternion_from_euler(0.0, 0.0, 0.0)
# 	moving4 = Moving("unob_3", Spawning1, x_position + ptFinal[0], y_position + ptFinal[1], z_position + ptFinal[2], oriFinal, unob_3)
# 	moving4.spawning()

# if __name__ == '__main__':
# 	uncluttered_objects()