import random
import string
from tkinter import Tk, Label, Entry, Button, END
from PIL import Image, ImageTk
from captcha.image import ImageCaptcha


def createImage(flag=0):
    """
    Generates and displays a new CAPTCHA image. If 'flag' is 1, the verification label is hidden.
    """
    global random_string, image_label, image_display, entry, verify_label

    # Hide verification label if the Reload button is pressed
    if flag == 1:
        verify_label.grid_forget()

    # Clear the input box
    entry.delete(0, END)

    # Generate a random CAPTCHA string
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    # Generate the CAPTCHA image
    image_captcha = ImageCaptcha(width=250, height=125)
    image_generated = image_captcha.generate_image(random_string)
    image_display = ImageTk.PhotoImage(image_generated)

    # Remove the old image and display the new one
    image_label.grid_forget()
    image_label = Label(root, image=image_display)
    image_label.grid(row=1, column=0, columnspan=2, padx=10)


def check(input_text, captcha_text):
    """
    Verifies if the user input matches the CAPTCHA text.
    Displays 'Verified' or 'Incorrect!' messages.
    """
    global verify_label

    # Clear any previous verification message
    verify_label.grid_forget()

    # Check if input matches the CAPTCHA
    if input_text.lower() == captcha_text.lower():
        verify_label = Label(master=root, text="Verified", font="Arial 15", bg='#ffe75c', fg="#00a806")
    else:
        verify_label = Label(master=root, text="Incorrect!", font="Arial 15", bg='#ffe75c', fg="#fa0800")
        createImage()  # Generate a new CAPTCHA on incorrect input

    verify_label.grid(row=0, column=0, columnspan=2, pady=10)


if __name__ == "__main__":
    # Initialize the Tkinter window
    root = Tk()
    root.title('Image Captcha')
    root.configure(background='#ffe75c')

    # Initialize global variables
    verify_label = Label(root)
    image_label = Label(root)

    # Input box for user to type the CAPTCHA
    entry = Entry(root, width=10, borderwidth=5, font="Arial 15", justify="center")
    entry.grid(row=2, column=0)

    # Generate and display the first CAPTCHA
    createImage()

    # Reload button with an image
    try:
        reload_img = ImageTk.PhotoImage(
            Image.open(r"C:\Users\user\Downloads\Captcha_Generator\refresh.png").resize((32, 32), Image.Resampling.LANCZOS)
        )
        reload_button = Button(image=reload_img, command=lambda: createImage(1))
        reload_button.grid(row=2, column=1, pady=10)
    except FileNotFoundError:
        print("Error: 'refresh.png' not found. Please ensure the file exists at the specified path.")

    # Submit button to verify the CAPTCHA
    submit_button = Button(root, text="Submit", font="Arial 10", command=lambda: check(entry.get(), random_string))
    submit_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Bind the Enter key to submit the CAPTCHA
    root.bind('<Return>', func=lambda Event: check(entry.get(), random_string))

    # Keep the window open
    root.mainloop()
