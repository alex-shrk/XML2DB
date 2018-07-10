import sys
import xml.etree.ElementTree as ET
import psycopg2


def open_connect_to_db(db):
    connect = psycopg2.connect(
        host=db.get('host'),
        port=db.get('port'),
        database=db.get('database'),
        user=db.get('user'),
        password=db.get('password')
    )
    return connect


def close_connect_to_db(connect):
    connect.close()


def get_id_file(cursor):
    query_id_file = """SELECT NEXTVAL('sec_id_file')"""
    cursor.execute(query_id_file)
    return int(cursor.fetchone()[0])  # get result of query


def insert_faces(root, connect, id_file):
    query_insert_faces = """INSERT INTO faces (id_file,x1,y1,z1,x2,y2,z2,x3,y3,z3,id_mat) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    cursor = connect.cursor()

    vertex_x = list()
    vertex_y = list()
    vertex_z = list()

    vertexCount = 0

    hasSharedGeometry = False
    rootSharedGeometry = root.find('sharedgeometry')
    if rootSharedGeometry:
        vertexCount = int(rootSharedGeometry.get('vertexcount'))
        for sharedGeometry in root.iter('sharedgeometry'):
            for vertex in sharedGeometry.iter('position'):
                vertex_x.append(float(vertex.get('x')))
                vertex_y.append(float(vertex.get('y')))
                vertex_z.append(float(vertex.get('z')))
        hasSharedGeometry = True

    for submesh in root.iter('submesh'):
        material = submesh.get('material')
        #print (material)

        if not hasSharedGeometry:
            rootGeometry = submesh.find('geometry')
            if rootGeometry is not None:
                vertexCount = int(rootGeometry.get('vertexcount'))
                for vertex in submesh.iter('position'):
                    vertex_x.append(float(vertex.get('x')))
                    vertex_y.append(float(vertex.get('y')))
                    vertex_z.append(float(vertex.get('z')))

        if len(vertex_x) and len(vertex_y) and len(vertex_z):
            for face in submesh.iter('face'):
                v1 = int(face.get('v1'))
                v2 = int(face.get('v2'))
                v3 = int(face.get('v3'))
                if (v1 < vertexCount and v2 < vertexCount and v3 < vertexCount):
                    values_faces = (
                        id_file, vertex_x[v1], vertex_y[v1], vertex_z[v1], vertex_x[v2], vertex_y[v2], vertex_z[v2],
                        vertex_x[v3], vertex_y[v3], vertex_z[v3], material)
                    cursor.execute(query_insert_faces, values_faces)
    connect.commit()
    cursor.close()


def insert_object(root, connect, id_file):
    query_insert_objects = """INSERT INTO objects (id_file,x,y,z,qw,qx,qy,qz,id_obj) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    cursor = connect.cursor()

    rootNodes = root.find('nodes')
    if rootNodes is not None:
        for node in root.iter('node'):
            name = node.get('name')
            #print (name)
            position = node.find('position')
            pos_x = float(position.get('x'))
            pos_y = float(position.get('y'))
            pos_z = float(position.get('z'))

            rotation = node.find('rotation')
            rot_w = float(rotation.get('qw'))
            rot_x = float(rotation.get('qx'))
            rot_y = float(rotation.get('qy'))
            rot_z = float(rotation.get('qz'))

            values_object = (
                id_file, pos_x, pos_y, pos_z, rot_w, rot_x, rot_y, rot_z, name)

            cursor.execute(query_insert_objects, values_object)
    connect.commit()
    cursor.close()


def insert(root, db):
    connect = open_connect_to_db(db)
    cursor = connect.cursor()
    id_file = get_id_file(cursor)
    insert_faces(root, connect, id_file)
    insert_object(root, connect, id_file)
    close_connect_to_db(connect)


def parse_xml(xmlFile, db):
    print('Start process..')
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    insert(root, db)
    print ('Complete')

def main(argv):

    if (len(argv)==0) or (argv[0] in ("-h", "--help")) :
        print ('xml2db.exe xmlfile <path to xml file> ' \
              'host <db host> port <db port> ' \
              'user <db user> password <db password>')
        sys.exit()
    else:
        xmlfile = argv[1]
        db_settings = {argv[2]: argv[3],
                       argv[4]: int(argv[5]),
                       'database': '3dScene',
                      argv[6]: argv[7],
                      argv[8]: argv[9]
        }
        parse_xml(xmlfile, db_settings)


if __name__ == '__main__':
    main(sys.argv[1:])
