import spidev
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
import subprocess
import time

# Pin configuration
RST_PIN = 27
DC_PIN = 25
BL_PIN = 18
SPI_BUS = 0
SPI_DEVICE = 0

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RST_PIN, GPIO.OUT)
GPIO.setup(DC_PIN, GPIO.OUT)
GPIO.setup(BL_PIN, GPIO.OUT)

# Initialize SPI
spi = spidev.SpiDev(SPI_BUS, SPI_DEVICE)
spi.max_speed_hz = 4000000

def lcd_command(cmd):
    GPIO.output(DC_PIN, GPIO.LOW)
    spi.xfer([cmd])

def lcd_data(data):
    GPIO.output(DC_PIN, GPIO.HIGH)
    spi.xfer([data])

def lcd_init():
    GPIO.output(RST_PIN, GPIO.HIGH)
    GPIO.output(RST_PIN, GPIO.LOW)
    GPIO.output(RST_PIN, GPIO.HIGH)
    
    lcd_command(0x36)
    lcd_data(0x70)

    lcd_command(0x3A)
    lcd_data(0x05)

    lcd_command(0xB2)
    lcd_data(0x0C)
    lcd_data(0x0C)
    lcd_data(0x00)
    lcd_data(0x33)
    lcd_data(0x33)

    lcd_command(0xB7)
    lcd_data(0x35)

    lcd_command(0xBB)
    lcd_data(0x19)

    lcd_command(0xC0)
    lcd_data(0x2C)

    lcd_command(0xC2)
    lcd_data(0x01)

    lcd_command(0xC3)
    lcd_data(0x12)

    lcd_command(0xC4)
    lcd_data(0x20)

    lcd_command(0xC6)
    lcd_data(0x0F)

    lcd_command(0xD0)
    lcd_data(0xA4)
    lcd_data(0xA1)

    lcd_command(0xE0)
    lcd_data(0xD0)
    lcd_data(0x04)
    lcd_data(0x0D)
    lcd_data(0x11)
    lcd_data(0x13)
    lcd_data(0x2B)
    lcd_data(0x3F)
    lcd_data(0x54)
    lcd_data(0x4C)
    lcd_data(0x18)
    lcd_data(0x0D)
    lcd_data(0x0B)
    lcd_data(0x1F)
    lcd_data(0x23)

    lcd_command(0xE1)
    lcd_data(0xD0)
    lcd_data(0x04)
    lcd_data(0x0C)
    lcd_data(0x11)
    lcd_data(0x13)
    lcd_data(0x2C)
    lcd_data(0x3F)
    lcd_data(0x44)
    lcd_data(0x51)
    lcd_data(0x2F)
    lcd_data(0x1F)
    lcd_data(0x1F)
    lcd_data(0x20)
    lcd_data(0x23)

    lcd_command(0x21)
    lcd_command(0x11)
    lcd_command(0x29)

def lcd_display_image(image):
    # Convert image to RGB format
    image = image.convert('RGB')
    pixel_data = list(image.getdata())

    lcd_command(0x2A)
    lcd_data(0x00)
    lcd_data(0x00)
    lcd_data(0x00)
    lcd_data(0x7F)

    lcd_command(0x2B)
    lcd_data(0x00)
    lcd_data(0x00)
    lcd_data(0x00)
    lcd_data(0x7F)

    lcd_command(0x2C)

    for pixel in pixel_data:
        r = pixel[0] >> 3
        g = pixel[1] >> 2
        b = pixel[2] >> 3
        pixel_word = (r << 11) | (g << 5) | b
        lcd_data(pixel_word >> 8)
        lcd_data(pixel_word & 0xFF)

def query_language_model(question):
    # Define the system message and template
    system_message = "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions."
    template = f"""<s>{system_message}</s>\n<s>Human:\n{question}</s>\n<s>Assistant:\n"""
    
    # Start the Ollama process
    process = subprocess.Popen(['ollama', 'run', 'qwen2-0_5b-instruct-q4_0.gguf'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Send the question to the model wrapped in the template
    process.stdin.write(template + '\n')
    process.stdin.flush()
    process.stdin.close()

    # Read the response from the model
    answer_lines = []
    while True:
        line = process.stdout.readline()
        if not line:
            break
        answer_lines.append(line.strip())

    # Capture any errors
    errors = process.stderr.read().strip()

    # Close the process
    process.stdout.close()
    process.stderr.close()
    process.wait()
    
    answer = "\n".join(answer_lines)
    return answer, errors

def display_answer_on_lcd(answer):
    # Initialize the LCD
    lcd_init()

    # Create a blank image for drawing
    image = Image.new('RGB', (128, 128), 'WHITE')
    draw = ImageDraw.Draw(image)

    # Draw the answer text (you may need to adjust text size and positioning)
    font = ImageFont.load_default()
    draw.text((10, 10), answer, fill='BLACK', font=font)

    # Display the image
    lcd_display_image(image)

if __name__ == '__main__':
    try:
        question = input("Enter your question: ")
        answer, errors = query_language_model(question)
        if errors:
            print("Error:", errors)
        else:
            print("Answer:", answer)
            display_answer_on_lcd(answer)
    finally:
        GPIO.cleanup()
