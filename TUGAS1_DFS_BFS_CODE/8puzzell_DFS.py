import numpy as np

class Node():
    def __init__(self,state,parent,action,depth,step_cost,path_cost,heuristic_cost):
        self.state = state 
        self.parent = parent 
        self.action = action 
        self.depth = depth
        self.step_cost = step_cost 
        self.path_cost = path_cost 
        self.heuristic_cost = heuristic_cost 
        
        self.move_up = None 
        self.move_left = None
        self.move_down = None
        self.move_right = None
    
    def try_move_down(self):
        zero_index=[i[0] for i in np.where(self.state==0)] 
        if zero_index[0] == 0:
            return False
        else:
            up_value = self.state[zero_index[0]-1,zero_index[1]] 
            new_state = self.state.copy()
            new_state[zero_index[0],zero_index[1]] = up_value
            new_state[zero_index[0]-1,zero_index[1]] = 0
            return new_state,up_value
        
    def try_move_right(self):
        zero_index=[i[0] for i in np.where(self.state==0)] 
        if zero_index[1] == 0:
            return False
        else:
            left_value = self.state[zero_index[0],zero_index[1]-1] 
            new_state = self.state.copy()
            new_state[zero_index[0],zero_index[1]] = left_value
            new_state[zero_index[0],zero_index[1]-1] = 0
            return new_state,left_value
        
    def try_move_up(self):
        zero_index=[i[0] for i in np.where(self.state==0)] 
        if zero_index[0] == 2:
            return False
        else:
            lower_value = self.state[zero_index[0]+1,zero_index[1]] 
            new_state = self.state.copy()
            new_state[zero_index[0],zero_index[1]] = lower_value
            new_state[zero_index[0]+1,zero_index[1]] = 0
            return new_state,lower_value
        

    def try_move_left(self):
        zero_index=[i[0] for i in np.where(self.state==0)] 
        if zero_index[1] == 2:
            return False
        else:
            right_value = self.state[zero_index[0],zero_index[1]+1] # value of the right tile
            new_state = self.state.copy()
            new_state[zero_index[0],zero_index[1]] = right_value
            new_state[zero_index[0],zero_index[1]+1] = 0
            return new_state,right_value

        
    # saat goal node ditemukan, lacak kembali sampai root node dan print pathnya
    def print_path(self):
        # membuat stack FILO untuk menempatkan trace
        state_trace = [self.state]
        action_trace = [self.action]
        depth_trace = [self.depth]
        step_cost_trace = [self.step_cost]
        path_cost_trace = [self.path_cost]
        heuristic_cost_trace = [self.heuristic_cost]
        
        # menambah informasi node pada saat backtracking tree
        while self.parent:
            self = self.parent

            state_trace.append(self.state)
            action_trace.append(self.action)
            depth_trace.append(self.depth)
            step_cost_trace.append(self.step_cost)
            path_cost_trace.append(self.path_cost)
            heuristic_cost_trace.append(self.heuristic_cost)

        # untuk print path
        step_counter = 0
        while state_trace:
            print ('step',step_counter)
            print (state_trace.pop())
            
            
            step_counter += 1
                        
    def depth_first_search(self, goal_state):

            queue = [self] # queue dari node yang ditemukan namun belum dikunjungi, FILO
            queue_num_nodes_popped = 0 #jumlah dari node yang di pop pada queue, mengukur performa waktu
            queue_max_length = 1 # jumlah node maksimum dalam queue

            depth_queue = [0] # queue untuk node depth
            path_cost_queue = [0] # queue untuk harga path
            visited = set([]) # mencatat state-state yang pernah dilalui

            while queue:
                # update panjang maksimum dari queue
                if len(queue) > queue_max_length:
                    queue_max_length = len(queue)

                current_node = queue.pop(0) # pilih dan pop node pertama dari queue
                queue_num_nodes_popped += 1 

                current_depth = depth_queue.pop(0) # pilih dan pop kedalaman dari node saat ini
                current_path_cost = path_cost_queue.pop(0) # # pilih dan pop harga path untuk mencapai node saat ini
                visited.add(tuple(current_node.state.reshape(1,9)[0])) # tambahkan state, yang direpresentasikan sebagai tuple
                
                # ketika goal state ditemukan, lakukan backtracking ke node root dan print pathnya
                if np.array_equal(current_node.state,goal_state):
                    current_node.print_path()

                    print ('Time performance:',str(queue_num_nodes_popped),'nodes popped off the queue.')
                    return True

                else:                
                    # cek apakah menggerakan kotak atas ke bawah adalah langkah yang valid
                    if current_node.try_move_down():
                        new_state,up_value = current_node.try_move_down()
                        # cek apakah node hasil sudah dikunjungi
                        if tuple(new_state.reshape(1,9)[0]) not in visited:
                            # membuat child node baru
                            current_node.move_down = Node(state=new_state,parent=current_node,action='down',depth=current_depth+1,\
                                                  step_cost=up_value,path_cost=current_path_cost+up_value,heuristic_cost=0)
                            queue.insert(0,current_node.move_down)
                            depth_queue.insert(0,current_depth+1)
                            path_cost_queue.insert(0,current_path_cost+up_value)

                    # cek apakah menggerakan kotak kiri ke kanan adalah langkah yang valid 
                    if current_node.try_move_right():
                        new_state,left_value = current_node.try_move_right()
                        # cek apakah node hasil sudah dikunjungi
                        if tuple(new_state.reshape(1,9)[0]) not in visited:
                            # membuat child node baru
                            current_node.move_right = Node(state=new_state,parent=current_node,action='right',depth=current_depth+1,\
                                                  step_cost=left_value,path_cost=current_path_cost+left_value,heuristic_cost=0)
                            queue.insert(0,current_node.move_right)
                            depth_queue.insert(0,current_depth+1)
                            path_cost_queue.insert(0,current_path_cost+left_value)

                    # cek apakah menggerakan kotak bawah ke atas adalah langkah yang valid
                    if current_node.try_move_up():
                        new_state,lower_value = current_node.try_move_up()
                         # cek apakah node hasil sudah dikunjungi
                        if tuple(new_state.reshape(1,9)[0]) not in visited:
                            # membuat child node baru
                            current_node.move_up = Node(state=new_state,parent=current_node,action='up',depth=current_depth+1,\
                                                  step_cost=lower_value,path_cost=current_path_cost+lower_value,heuristic_cost=0)
                            queue.insert(0,current_node.move_up)
                            depth_queue.insert(0,current_depth+1)
                            path_cost_queue.insert(0,current_path_cost+lower_value)

                    # cek apakah menggerakan kotak kanan ke kiri adalah langkah yang valid 
                    if current_node.try_move_left():
                        new_state,right_value = current_node.try_move_left()
                        # cek apakah node hasil sudah dikunjungi
                        if tuple(new_state.reshape(1,9)[0]) not in visited:
                            # membuat child node baru
                            current_node.move_left = Node(state=new_state,parent=current_node,action='left',depth=current_depth+1,\
                                                  step_cost=right_value,path_cost=current_path_cost+right_value,heuristic_cost=0)
                            queue.insert(0,current_node.move_left)
                            depth_queue.insert(0,current_depth+1)
                            path_cost_queue.insert(0,current_path_cost+right_value)
               
                        
   
test = np.array([1,8,2,0,4,3,7,6,5]).reshape(3,3)

initial_state = test
goal_state = np.array([1,2,3,4,5,6,7,8,0]).reshape(3,3)
print (initial_state, '\n')
print (goal_state)

root_node = Node(state=initial_state, parent=None,action=None,depth=0,step_cost=0,path_cost=0,heuristic_cost=0)

# search level by level with queue
root_node.depth_first_search(goal_state)
#root_node.depth_first_search(goal_state)