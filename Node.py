
class Node:
    def __init__(self, name, codigo_departamento):
        self.name = name
        self.codigo_departamento = codigo_departamento
        self.next = None
        self.prev = None
        self.sublista = [] 

class MultiLista:
    def __init__(self):
        self.cabeza = None
    
    def insertar(self, name, codigo_departamento):
        
        # Verificar si ya existe un nodo con ese nombre/código
        if self._buscar_nodo_por_codigo(codigo_departamento):
            return  # Ya existe, no insertamos
            
        nuevo_nodo = Node(name, codigo_departamento)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            nuevo_nodo.next = self.cabeza
            self.cabeza.prev = nuevo_nodo
            self.cabeza = nuevo_nodo
    
    def agregar_sublista(self, codigo_departamento, elemento_municipio):
        """Agrega un elemento (Municipio/Área) a la sublista de un nodo (Departamento)
           usando el código del departamento."""
        nodo = self._buscar_nodo_por_codigo(codigo_departamento)
        if nodo:
            nodo.sublista.append(elemento_municipio)
    
    def _buscar_nodo_por_nombre(self, name):
        """Busca un nodo por nombre (Departamento)"""
        actual = self.cabeza
        while actual:
            if actual.name == name:
                return actual
            actual = actual.next
        return None
        
    def _buscar_nodo_por_codigo(self, codigo_departamento):
        """Busca un nodo por código de departamento"""
        actual = self.cabeza
        while actual:
            if actual.codigo_departamento == codigo_departamento:
                return actual
            actual = actual.next
        return None
    
    def mostrar(self):
        """Muestra todos los nodos y sus sublistas (solo los nombres y el total de municipios)"""
        actual = self.cabeza
        while actual:
            print(f"Departamento: {actual.name} ({actual.codigo_departamento}), Municipios: {len(actual.sublista)}")
            # Si quieres ver los municipios, descomenta la siguiente línea:
            # print(f"  -> Sublista: {[m['Nombre Municipio'] for m in actual.sublista]}")
            actual = actual.next

# La parte de ejemplo que tenías al final se elimina para enfocarnos en la carga del CSV
# ml = MultiLista()
# ml.insertar("Nodo1")
# ml.insertar("Nodo2")
# ml.agregar_sublista("Nodo1", "Elemento1")
# ml.agregar_sublista("Nodo1", "Elemento2")
# ml.agregar_sublista("Nodo2", "ElementoA")
# ml.mostrar()