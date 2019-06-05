def save_session_to_frozen_pb(sess, save_dir, output_node_names, output_graph_name, variable_names_blacklist=""):
    
    checkpoint_prefix = "saved_checkpoint"
    checkpoint_state_name = "checkpoint_state"
    input_graph_name = "input_graph.pb"
    save_dir = "."
    
    # Save the weights from the session to a checkpoint file
    saver = saver_lib.Saver()
    checkpoint_path = saver.save(
        K.get_session(),
        checkpoint_prefix,
        global_step=0,
        latest_filename=checkpoint_state_name)

    # Save the graph architecture to a pb file
    graph_io.write_graph(K.get_session().graph, save_dir, input_graph_name)

    # Create list of output nodes
    reset_ops_names = [n.name for n in reset_ops]
    reset_ops_string = ",".join(reset_ops_names).replace(":0", "")
    update_ops_names = [n.name for n in update_ops]
    update_ops_string = ",".join(update_ops_names).replace(":0", "")

    output_node_names = output_tensor.name.replace(":0", "") + "," + reset_ops_names + "," + update_ops_string

    # Collect the state variables to preserve
    state_variables = []
    for layer in stateful_model.layers:
        for old_value, new_value in layer.updates:
            state_variables.append(old_value)
    state_variables_names = [n.name for n in state_variables]
    state_variables_string = ",".join(state_variables_names).replace(":0", "")
    variable_names_blacklist = state_variables_string

    # Freeze the graph
    input_graph_path = input_graph_name
    input_saver_def_path = ""
    input_binary = False
    restore_op_name = "save/restore_all"
    filename_tensor_name = "save/Const:0"
    output_graph_name = "stateful_model.pb"
    clear_devices = False
    freeze_graph.freeze_graph(input_graph_path, input_saver_def_path,
                              input_binary, checkpoint_path, output_node_names,
                              restore_op_name, filename_tensor_name,
                              output_graph_name, clear_devices, "", variable_names_blacklist)


    [print(n.name) for n in tf.get_default_graph().as_graph_def().node]