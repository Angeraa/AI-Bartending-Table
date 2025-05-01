from vosk import Model, KaldiRecognizer
import pyaudio
from config import MODEL_PATH
from bartending import drinkMaker

#main loop
def main():
	model = Model(MODEL_PATH)
	recog = KaldiRecognizer(model, 16000)
	mic = pyaudio.PyAudio()
	stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
	stream.start_stream()

	drink_maker = drinkMaker.DrinkMaker()

	trigger = False
	action_words = {"make", "pour", "get"}

	drink_func = {frozenset(['manhattan']): lambda: drink_maker.pump_drink([2,0], [60,30]), frozenset(["margarita"]): lambda: drink_maker.pump_drink([1,9,11], [54, 30, 24]),
				frozenset(["hanky", "panky"]): lambda: drink_maker.pump_drink([6, 0], [45, 45]), frozenset(["rum", "pepsi"]): lambda: drink_maker.pump_drink([3, 8], [30, 150]),
				frozenset(["red", "wine"]): lambda: drink_maker.pump_drink([5], [180], is_wine=True), frozenset(["white", "wine"]): lambda: drink_maker.pump_drink([4], [180], is_wine=True),
				frozenset(["mojito"]): lambda: drink_maker.pump_drink([3,9], [60, 30]), frozenset(["negroni"]): lambda: drink_maker.pump_drink([0, 6, 10], [30, 30, 30]),
				frozenset(["daiquiri"]): lambda: drink_maker.pump_drink([3,9], [60, 24]), frozenset(["old", "fashioned"]): lambda: drink_maker.pump_drink([2], [75]),
				frozenset(["just", "whiskey"]): lambda: drink_maker.pump_drink([2], [30]),
				frozenset(["gin", "tonic"]): lambda: drink_maker.pump_drink([6,7], [30, 120]), frozenset(["just", "lemonade"]): lambda: drink_maker.pump_drink([8], [200])} 
				#pass in the keywords and drink functions, add more drink functions

	while True:
		data = stream.read(4096)
		#if len(data) == 0:
		#	break
		try:
			if recog.AcceptWaveform(data):
				text = recog.Result()[14:-3]
				print(text)
					
				if trigger == True:
					words = set(text.split())
					if words.issuperset({"forget", "it", "bartender"}):
						trigger = False
					else:				
						for keyword in drink_func.keys():
							if not words.isdisjoint(action_words) and words.issuperset(keyword):
								print(keyword)
								drink_maker.greenLED.blink(0.5, 0.5)
								drink_func[keyword]()
								trigger = False
								break
							
				if "okay bartender" in text:
					trigger = True
					drink_maker.greenLED.on()
					print("What do ya want")
							
			if trigger == False:
				drink_maker.greenLED.off()
			if drink_maker.cpu.temperature > 85:
				drink_maker.redLED.blink(1, 1)
			else:
				drink_maker.redLED.off()
		except Exception as e:
			print(e)
			drink_maker.close()
			stream.close()
			mic.terminate()
			break
			
if __name__ == "__main__":
	main()