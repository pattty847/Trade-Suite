from program import Program
from viewport import View_Port
import logging


logging.basicConfig(
    level=logging.INFO, 
    filename="info_logs.log", 
    filemode="a", 
    format='%(asctime)s - %(message)s', 
    datefmt='%d-%b-%y %H:%M:%S'
)



if __name__ == "__main__":
    # logging.info("-----------------------------------------------")
    # logging.info("Starting Trade Suite...")
    # trade_suite = TradeSuite()
    # trade_suite.configure_dpg()
    
    # Main entry point to program
    with View_Port(title='Custom Title') as viewport:
        # window = Window('win', viewport.tag, viewport.aggr).build()
        
        # Define our Program class, passing it the viewport, and call build_ui()
        program = Program(viewport).build_ui()
        
        # This will run the dearpygui loop for the program (call after UI elements are built)
        viewport.run()