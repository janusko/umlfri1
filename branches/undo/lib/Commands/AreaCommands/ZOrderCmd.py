from lib.Commands import CBaseCommand


class CZOrderCmd(CBaseCommand):
    def __init__(self, diagram, action, canvas, description = None): 
        CBaseCommand.__init__(self, description)
        self.diagram = diagram
        self.action = action
        self.canvas = canvas
        
        self.selection = []
        for element in self.diagram.GetSelected():
            self.selection.append(element)


    def do (self):
        if (self.action == 'SendBack'):
            self.diagram.ShiftElementsBack(self.canvas)
                    
        elif (self.action == 'BringForward'):
            self.diagram.ShiftElementsForward(self.canvas)
                    
        elif (self.action == 'ToBottom'):
            self.diagram.ShiftElementsToBottom()
                    
        elif (self.action == 'ToTop'):
            self.diagram.ShiftElementsToTop()
        
        else:
            self.enabled = False
            
        #if self.description == None:
            #if (self.action == 'SendBack'):
                #print_action = 'Sending selection back'
            
            #elif (self.action == 'BringForward'):
                #print_action =  'Bringing selection back'
            
            #elif (self.action == 'ToBottom'):
                #print_action = 'Sending selection to bottom' 
            
            #elif (self.action == 'ToTop'):
                #print_action = 'Bringing selection to top'            
                
            #self.description = _('%s on %s') %(print_action, self.diagram.GetName())


    def undo(self):
        current_selection=[]
        for element in self.diagram.GetSelected():
            current_selection.append(element)

        self.diagram.DeselectAll()
        
        for element in self.selection:
           self.diagram.AddToSelection(element)

        if (self.action == 'SendBack'):
            self.diagram.ShiftElementsForward(self.canvas)
        
        elif (self.action == 'BringForward'):
            self.diagram.ShiftElementsBack(self.canvas)            
            
        elif (self.action == 'ToBottom'):
            self.diagram.ShiftElementsToTop()
        
        elif (self.action == 'ToTop'):
            self.diagram.ShiftElementsToBottom()

        self.diagram.DeselectAll()  
        
        for element in current_selection:
            self.diagram.AddToSelection(element)


    def getDescription(self):
        if self.description != None:
            return self.description
        else:
            if (self.action == 'SendBack'):
                print_action = 'Sending selection back'
            
            elif (self.action == 'BringForward'):
                print_action =  'Bringing selection back'
            
            elif (self.action == 'ToBottom'):
                print_action = 'Sending selection to bottom' 
            
            elif (self.action == 'ToTop'):
                print_action = 'Bringing selection to top' 
                
            return _('%s on %s') %(print_action, self.diagram.GetName())
            