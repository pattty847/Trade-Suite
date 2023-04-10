from program import Program
from viewport import View_Port
import logging
import argparse

logging.basicConfig(
    level=logging.INFO, 
    filename="info_logs.log", 
    filemode="a", 
    format='%(asctime)s - %(message)s', 
    datefmt='%d-%b-%y %H:%M:%S'
)

def parse_args():
    parser = argparse.ArgumentParser(description="Run the program with optional arguments.")
    parser.add_argument('--charts', action='store_true', help='Display charts')
    parser.add_argument('--exchange', type=str, help='Exchange name (e.g., coinbasepro)')
    parser.add_argument('--symbol', type=str, help='Symbol (e.g., BTC/USD)')
    parser.add_argument('--timeframe', type=str, help='Timeframe for the chart (e.g., 1m, 1h, 1d)')
    return parser.parse_args()

if __name__ == "__main__":
    
    args = parse_args()

    # Main entry point to program
    with View_Port(title='Custom Title') as viewport:
        # window = Window('win', viewport.tag, viewport.aggr).build()
        
        # Define our Program class, passing it the viewport, and call build_ui()
        program = Program(viewport)
        program.build_ui()
        
        if args.charts:
            program.chart.draw_chart(args.exchange, args.symbol, args.timeframe) # Run this command if -main parameter is passed
        
        # This will run the dearpygui loop for the program (call after UI elements are built)
        viewport.run()