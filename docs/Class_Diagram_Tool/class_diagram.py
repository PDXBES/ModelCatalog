import re
import os
import subprocess

# Calls batch file to run pyreverse
try:
    subprocess.call("class_diagram.bat")
except:
    print("Failed to run pyReverse")
    quit()

output_format = "svg"  # pdf svg png etc. see https://graphviz.gitlab.io/_pages/doc/info/output.html
control_files = []
executable_path = os.path.dirname(os.path.realpath(__file__))
for file in os.listdir(executable_path + "\\" + "Control_Files"):
    if file.endswith(".csv"):
        control_files.append(file)

dot_file = "classes.dot"
dot_file_no_ext = dot_file[0:len(dot_file) - 4]
for control_file in control_files:
    try:
        control_file_no_ext = control_file[0:len(control_file) - 4]
        dot_file_out = "final" + control_file_no_ext + ".dot"
        dot_file_names_only_out = "names_only_final" + control_file_no_ext + ".dot"

        fin = open(dot_file, 'r')
        fin_control = open("Control_Files" + "\\" + control_file, 'r')
        fout = open(dot_file_out, 'w')
        fout_name_only = open(dot_file_names_only_out, 'w')

        column_names = []
        columns = []
        names = []
        connections = []
        inheritances = []

        line = fin_control.readline()
        column_names_line = line.split(',')
        for token in column_names_line:
            column_names.append(token)
            columns.append([])

        line = fin_control.readline()
        dummy_record_name_count = 0
        while line:
            record_names_and_parents = line.split(',')
            count = 0
            for record_name_and_parents in record_names_and_parents:
                if '(' in record_name_and_parents:
                    record_name = re.split('[(,)]', record_name_and_parents)[0]
                    parents = re.split('[(,)]', record_name_and_parents)[1].split(';')
                    inheritances.append(parents)
                else:
                    record_name = record_name_and_parents
                    inheritances.append([])
                record_name = record_name.strip('\n')
                record_name = record_name.strip()
                if record_name == "*":
                    record_name = "_d" + str(dummy_record_name_count)
                    dummy_record_name_count += 1
                record_name = record_name.strip('\n')
                columns[count].append(record_name)
                names.append(record_name)
                connections.append([])
                count += 1
            line = fin_control.readline()

        fin_control.close()

        line = fin.readline()
        fout.write(line)
        fout_name_only.write(line)
        line = fin.readline()
        fout.write(line)
        fout_name_only.write(line)
        line = fin.readline()
        line = fin.readline()

        # Write format information
        fout.write("nodesep=0.5;\n")
        fout_name_only.write("nodesep=0.5;\n")
        fout.write("rankdir=\"TB\";\n")
        fout_name_only.write("rankdir=\"TB\";\n")
        fout.write("edge [ constraint=False ];\n")
        fout_name_only.write("edge [ constraint=False ];\n")
        #fout_name_only.write("ratio = 0.65;\n")
        #fout_name_only.write("size = \"8.5, 11\";\n")
        #fout.write("ranksep=equally;\n")
        #fout_name_only.write("ranksep=equally;\n")
        fout.write("splines=\"ortho\";\n")
        fout_name_only.write("splines=\"ortho\";\n")

        # Write class object records with class names for labels rather than numbers
        while line:
            tokens = line.split('[')
            test = tokens[1][0:5]
            if test == 'label':
                tokens1 = tokens[1].split('{')
                if '|' in tokens1[1]:
                    name, attributes_and_types, methods = tokens1[1].split('|')
                    attributes = []
                    for attribute_and_type in attributes_and_types.split('\l'):
                        if ':' in attribute_and_type:
                            attribute, attribute_type = attribute_and_type.split(':')
                            if attribute_type != " MagicMock":
                                attributes.append(re.sub('_', '', attribute.strip()))
                        else:
                            attribute = attribute_and_type
                            attributes.append(re.sub('_', '', attribute.strip()))
                    attributesUpper = [a.upper() for a in attributes]
                    for connection_name in names:
                        list_connection_name = connection_name + "s"
                        if name in names:
                            index = names.index(name)
                            if connection_name.upper() in attributesUpper or list_connection_name.upper() in attributesUpper:
                               connections[index].append(connection_name)

            elif test == 'fontc':
                tokens1 = tokens[1].split(',')[1]
                tokens2 = tokens1.split('{')
                if '|' in tokens2[1]:
                    name, attributes_and_types, methods = tokens2[1].split('|')
                    attributes = []
                    for attribute_and_type in attributes_and_types.split('\l'):
                        if ':' in attribute_and_type:
                            attribute, attribute_type = attribute_and_type.split(':')
                            if attribute_type != " MagicMock":
                                attributes.append(re.sub('_', '', attribute.strip()))
                        else:
                            attribute = attribute_and_type
                            attributes.append(re.sub('_', '', attribute.strip()))
                    attributesUpper = [a.upper() for a in attributes]
                    for connection_name in names:
                        list_connection_name = connection_name + "s"
                        if name in names:
                            index = names.index(name)
                            if connection_name.upper() in attributesUpper or list_connection_name.upper() in attributesUpper:
                               connections[index].append(connection_name)
            else:
                break
            if name in names:
                new_line = "\"" + name + "\" [" + tokens[1]
                fout.write(new_line)
                new_line_names_only = "\"" + name + "\"[label= \"" + name + "\" , shape=\"record\"];\n"
                fout_name_only.write(new_line_names_only)
            line = fin.readline()
        fin.close()

        # write dummy records
        fout.write("\n")
        fout_name_only.write("\n")
        for column in columns:
            for record_name in column:
                if record_name[0:2] == "_d":
                    name = "\"" + record_name + "\""
                    label = "\"" + record_name + "\""
                    dummy_record = name + " [label=" + label + ", shape=\"record\" style=invis];\n"
                    fout.write(dummy_record)
                    fout_name_only.write(dummy_record)
        # write columns
        fout.write("\n")
        fout_name_only.write("\n")
        for column in columns:
            column_line = "{rank= tb "
            column_string = None
            for record_name in column:
                if column_string != None:
                    column_string += "->"
                else:
                    column_string = ""
                column_string += "\"" + record_name + "\""
            column_line += column_string
            column_line += " [constraint=true style=invis]};\n"
            fout.write(column_line)
            fout_name_only.write(column_line)
        # write column order
        column_order_line = "{rank= same "
        record_name_string = None
        for column in columns:
            record_name = column[1]
            if record_name_string == None:
                record_name_string = ""
                record_name_string += record_name
            else:
                record_name_string += "->" + record_name

        column_order_line += record_name_string
        column_order_line += " [constraint=True style=invis]};\n"
        fout.write(column_order_line)
        fout_name_only.write(column_order_line)

        # write connectors
        for connection, name in zip(connections, names):
            for connector in connection:
                fout.write("\"" + connector + "\"->\"" + name + "\";\n")
                fout_name_only.write("\"" + connector + "\"->\"" + name + "\";\n")
        # write inheritance connectors
        for inheritance, name in zip(inheritances, names):
            for parent in inheritance:
                fout.write("\"" + parent + "\"->\"" + name + "\" [color=\"green\"];\n")
                fout_name_only.write("\"" + parent + "\"->\"" + name + "\" [color=\"green\"];\n")
        # write closing curly bracket
        fout.write("}")
        fout_name_only.write("}")
        fout.close()
        fout_name_only.close()
    except:
        print "Failed to create dot for control file: " + control_file

    try:
        cmd1 = "dot -T" + output_format + " " + dot_file_names_only_out + " -o " + control_file_no_ext + "_names_only"  + "." + output_format
        subprocess.call(cmd1)
        cmd2 = "dot -T" + output_format + " " + dot_file_out + " -o " + control_file_no_ext + "." + output_format
        subprocess.call(cmd2)
    except:
        print "Failed to generate output from Graphviz for control file: " + control_file

try:
    cmd3 = "dot -T" + output_format + " " + dot_file + " -o " + dot_file_no_ext + "." + output_format
    subprocess.call(cmd3)
except:
    print "Failed to generate output from Graphviz for classes.dot."