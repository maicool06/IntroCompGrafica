class obj:
    def __init__(self):
        self.vertFaces = []
        self.normalFaces = []
        self.texturesFaces = []


    def objLoad(self, cant_elem, path_animation, name_animation):
        
        objList = []
        
        for x in range(0, cant_elem + 1):
            obje = obj()
            obje.__objParser( path_animation + name_animation + str(x) +".obj")
            objList.append( obje )
        
        return objList

    def __objParser(self, path):
        objFile = open(path, 'r')
        #objFile = open('box.obj', 'r')

        vertexList = []
        normalList = []
        textList = []

        for line in objFile:
            split = line.split()
            
            if len(split):
                if split[0] == "v":			 	# Si empieza con v, lo agrego a la lista de vertices				
                    vertex = [ float(split[1]), float(split[2]), float(split[3]) ]
                    vertexList.append(vertex)
                
                elif split[0] == "vn":			# Si empieza con vn, lo agrego a la lista de normales	
                    normal = [ float(split[1]), float(split[2]), float(split[3]) ]
                    normalList.append(normal)

                elif split[0] == "vt":            # Si empieza con vn, lo agrego a la lista de normales				
                    texture = [ float(split[1]), float(split[2]) ]
                    textList.append(texture)

                elif split[0] == "f":			# Si empieza con f, lo agrego a la lista de faces
                    vert = []
                    norm = []
                    text = []

                    for i in range(1,4):
                        splitFace = split[i].split("/")
                        vert.append(splitFace[0])
                        norm.append(splitFace[1])
                        text.append(splitFace[2])

                    if ( int(vert[0]) - 1 < len(vertexList ) and int(vert[1]) - 1 < len(vertexList ) and int(vert[2]) - 1 < len(vertexList )):
                        vertexface = [ vertexList[int(vert[0])-1], vertexList[int(vert[1])-1], vertexList[int(vert[2])-1] ]
                        self.vertFaces.append(vertexface)
                    
                    if ( int(norm[0]) - 1 < len(normalList ) and int(norm[1]) - 1 < len(normalList ) and int(norm[2]) - 1 < len(normalList )):
                        normalFace = [ normalList[int(norm[0])-1], normalList[int(norm[1])-1], normalList[int(norm[2])-1] ]
                        self.normalFaces.append(normalFace)
                    
                    if ( int(text[0]) - 1 < len(textList ) and int(text[1]) - 1 < len(textList ) and int(text[2]) - 1 < len(textList )):
                        textFace = [ textList[int(text[0])-1], textList[int(text[1])-1], textList[int(text[2])-1] ]
                        self.texturesFaces.append(textFace)                            
                
                else:
                    continue