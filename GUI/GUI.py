from reportlab.lib import colors
from tensorflow.keras.models import load_model
import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageDraw, ImageFont
import classification
import segmentation
import cv2 as cv
import os
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import time
os.environ["SM_FRAMEWORK"] = "tf.keras"
import segmentation_models


class EyeCareApp:
    def __init__(self, root):

        self.class_model_thread = classification.CustomThread(target=load_model, args=("classification.keras",))
        self.optic_model_thread = classification.CustomThread(target=load_model, args=("disk_cup_segmentation.keras",))
        self.vessel_model_thread = classification.CustomThread(target=load_model, args=("vessel_segmentation.keras",))

        self.optic_model_thread.start()
        self.class_model_thread.start()
        self.vessel_model_thread.start()

        self.optic_model = None
        self.class_model = None
        self.vessel_model = None

        self.original_image = None
        self.masked_image = None
        self.disease = None

        self.img_path = ""
        self.root = root
        self.root.title("EyeCare")
        self.root.geometry("700x600")
        self.root.iconbitmap("/static_files/icon.ico")
        ctk.set_appearance_mode("light")  # You can change to "dark" to see the dark mode
        ctk.set_default_color_theme("blue")

        self.main_frame = ctk.CTkFrame(root, corner_radius=10,fg_color=("white", "#2B2B2B"))
        self.classification_result_frame = ctk.CTkFrame(root, corner_radius=10, fg_color=("white", "#2B2B2B"))
        self.segmentation_result_frame = ctk.CTkFrame(root, corner_radius=10, fg_color=("white", "#2B2B2B"))
        self.img_section_frame = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color=("white", "#2B2B2B"), width=250, height=250)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

        # segmentation labels
        self.im1_label = ctk.CTkLabel(self.segmentation_result_frame, text="", corner_radius=20)
        self.im1_label.place(relx=0.05, rely=0.25, width=300, height=300, anchor="nw")

        self.im2_label = ctk.CTkLabel(self.segmentation_result_frame, text="", corner_radius=20)
        self.im2_label.place(relx=0.95, rely=0.25, width=300, height=300, anchor="ne")

        # Logo and Title
        self.logo_img = Image.open("/static_files/app_logo.png")
        self.logo_img = self.logo_img.resize((600, 120))
        self.logo_img = ctk.CTkImage(light_image=self.logo_img, dark_image=self.logo_img, size=(600, 120))

        self.upload_img = Image.open("/static_files/upload_sign.png")
        self.upload_img = ctk.CTkImage(light_image=self.upload_img, dark_image=self.upload_img, size=(50, 50))

        self.img_frame = Image.open("/static_files/img_frame.png")
        self.img_frame = ctk.CTkImage(light_image=self.img_frame, dark_image=self.img_frame, size=(250, 250))

        self.delete_img_icon = Image.open("/static_files/delete.png")
        self.delete_img_icon = ctk.CTkImage(dark_image=self.delete_img_icon, light_image=self.delete_img_icon, size=(20, 20))

        self.logo_label1 = ctk.CTkLabel(self.main_frame, image=self.logo_img, text="")
        self.logo_label2 = ctk.CTkLabel(self.classification_result_frame, image=self.logo_img, text="")
        self.logo_label3 = ctk.CTkLabel(self.segmentation_result_frame, image=self.logo_img, text="")

        self.logo_label1.place(relx=0.5, rely=0.12, anchor="center")
        self.logo_label2.place(relx=0.5, rely=0.12, anchor="center")
        self.logo_label3.place(relx=0.5, rely=0.12, anchor="center")

        self.printer_img = Image.open("/static_files/printer.png")
        self.printer_img = ctk.CTkImage(dark_image=self.printer_img, light_image=self.printer_img, size=(30, 30))

        self.home_img = Image.open("/static_files/home.png")
        self.home_img = ctk.CTkImage(dark_image=self.home_img, light_image=self.home_img, size=(30, 30))

        self.result_img = ctk.CTkLabel(self.classification_result_frame, text="", corner_radius=10)
        self.result_img.place(relx=0.5, rely=0.5, anchor="center", width=250, height=250)

        self.result_label = ctk.CTkLabel(self.classification_result_frame,
                                         text = "Based on the findings the patient maybe has :",
                                         font=("Arial", 16, "bold"),
                                         fg_color=("white", "blake"),
                                         bg_color=("black", "white"))
        self.result_label.place(relx=0.5, rely=0.78, anchor="s")

        self.result2_label = ctk.CTkLabel(self.classification_result_frame, text="",
                                          font=("Arial", 16, "bold"),
                                          fg_color=("white", "blake"),
                                          bg_color=("black", "white"))
        self.result2_label.place(relx=0.5, rely=0.79, anchor="center")

        # Drag & Drop area
        self.img_label = ctk.CTkLabel(self.img_section_frame, text="", corner_radius=10)
        self.delete_img_button = ctk.CTkButton(self.img_section_frame, image=self.delete_img_icon,
                                               corner_radius=100, text="", command=self.delete_img, width=5, height=5,
                                               border_width=0, fg_color="black", bg_color="black")

        self.img_label.place(relx=0.5, rely=0.5, anchor="center", width=250, height=250)
        self.delete_img_button.place(relx=0.90, rely=0.03, anchor="ne")

        self.upload_frame = ctk.CTkFrame(self.main_frame, width=250, height=250,
                                         corner_radius=10, fg_color=("white", "#2B2B2B"))
        self.upload_frame.place(relx=0.1, rely=0.35, anchor="nw")

        self.img_frame_label = ctk.CTkLabel(self.upload_frame, width=250, height=250,
                                            corner_radius=20, image=self.img_frame, text="")
        self.img_frame_label.place(relx=0.5, rely=0.5, anchor="center")

        self.upload_label_img = ctk.CTkLabel(self.upload_frame, image=self.upload_img,
                                             fg_color=("#E6F6FF", "#293239"), text="")
        self.upload_label_img.place(relx=0.5, rely=0.25, anchor="center")

        self.upload_label = ctk.CTkLabel(self.upload_frame, text="Drag & Drop\nor", font=("Arial", 14, "bold"),
                                         fg_color=("#E6F6FF", "#293239"), text_color=("#C6C2C2", "white"))
        self.upload_label.place(relx=0.5, rely=0.5, anchor="center")

        self.browse_button = ctk.CTkButton(self.upload_frame, text="Browse Files", command=self.browse_files,
                                           fg_color="#5597CD", bg_color=("#E8F1F8", "#293239"), corner_radius=15)
        self.browse_button.place(relx=0.5, rely=0.75, anchor="center")

        self.print_button1 = ctk.CTkButton(self.classification_result_frame, image= self.printer_img,
                                           text="Print Report", compound="left",
                                           font=("Arial", 18, "bold"), command=self.print_report, corner_radius=15)
        self.print_button1.place(relx=0.5, rely=0.95, anchor="center", width=200, height=50)

        self.home_button1 = ctk.CTkButton(self.classification_result_frame, image= self.home_img,
                                          text="Home", compound="left",
                                          font=("Arial", 18, "bold"),
                                          command=lambda : self.back_home(self.classification_result_frame),
                                          corner_radius=15)
        self.home_button1.place(relx=0.5, rely=0.85, anchor="center", width=200, height=50)

        self.print_button2 = ctk.CTkButton(self.segmentation_result_frame, image=self.printer_img,
                                           text="Print Report", compound="left",
                                           font=("Arial", 18, "bold"), command=self.print_report, corner_radius=15)
        self.print_button2.place(relx=0.5, rely=0.95, anchor="center", width=200, height=50)

        self.home_button2 = ctk.CTkButton(self.segmentation_result_frame, image=self.home_img,
                                          text="Home", compound="left",
                                          font=("Arial", 18, "bold"),
                                          command=lambda : self.back_home(self.segmentation_result_frame),
                                          corner_radius=15)
        self.home_button2.place(relx=0.5, rely=0.85, anchor="center", width=200, height=50)

        # Bind drag and drop functionality
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop)

        # Buttons
        self.buttons_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color=("white", "#2B2B2B"))
        self.buttons_frame.place(relx=0.90, rely=0.4, anchor="ne")

        self.classification_button = ctk.CTkButton(self.buttons_frame, text="Classification",
                                                   font=("Arial", 18, "bold"), fg_color="#5597CD",
                                                   command=self.classification, corner_radius=20)
        self.classification_button.place(relx=0.5, rely=0.2, anchor="center", width=200, height=50)

        self.optic_disk_button = ctk.CTkButton(self.buttons_frame, text="Optic Disk \nSegmentation",
                                               font=("Arial", 18, "bold"), fg_color="#5597CD",
                                               command=self.optic_disk_segmentation, corner_radius=20)
        self.optic_disk_button.place(relx=0.5, rely=0.5, anchor="center", width=200, height=50)

        self.vessel_segmentation_button = ctk.CTkButton(self.buttons_frame, text="Vessel \nSegmentation",
                                                        font=("Arial", 18, "bold"), fg_color="#5597CD",
                                                        command=self.vessel_segmentation, corner_radius=20)
        self.vessel_segmentation_button.place(relx=0.5, rely=0.8, anchor="center", width=200, height=50)

        # Appearance mode switch
        self.mode_switch = ctk.CTkSwitch(self.main_frame, text="Dark Mode", command=self.toggle_mode)
        self.mode_switch.place(relx=0.99, rely=0.95, anchor="ne")

    def delete_img(self):
        print("delete...")
        self.img_section_frame.place_forget()
        self.upload_frame.place(relx=0.1, rely=0.35, anchor="nw")

    def toggle_mode(self):
        if self.mode_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def back_home(self, frame):
        print("back...")
        frame.place_forget()
        self.img_section_frame.place_forget()
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=700, height=600)
        self.upload_frame.place(relx=0.1, rely=0.35, anchor="nw")

    def print_report(self, output_path="report.pdf"):
        try:
            c = canvas.Canvas(output_path, pagesize=letter)
            width, height = letter  # Size of the page
            print(width, height)

            # add title
            c.setFont("Helvetica", 30)
            text = "EyeCare Report"
            c.drawString(195, 735, text)

            # add full image
            image = ImageReader(self.original_image)
            image_width, image_height = 300, 300
            c.drawImage(image, 160, 350, width=image_width, height=image_height)

            # add text in classification case
            if self.disease is not None:
                c.setFont("Helvetica", 18)
                text = "Based on the findings the patient maybe has \n"
                c.drawString(100, 300, text)
                c.setFont("Helvetica", 18)
                c.setFillColor(colors.red)
                text = self.disease
                c.drawString(255, 275, text)
                self.disease = None

            if self.masked_image is not None:
                mask = ImageReader(self.masked_image)
                image_width, image_height = mask.getSize()
                offset = 0
                if image_width == 100:
                    offset = 100

                c.drawImage(mask, 160+offset, 30, width=image_width, height=image_height)
                self.masked_image = None

            c.showPage()
            c.save()

            if os.name == 'nt':  # Windows
                os.startfile(output_path, "print")
            elif os.name == 'posix':  # MacOS or Linux
                os.system("lpr " + output_path)
            else:
                print("OS not supported!")
        except Exception as e:
            print(f"Error printing report: {e}")

    def browse_files(self):
        self.img_path = filedialog.askopenfilename()
        print(f"File selected: {self.img_path}")
        self.display_image(self.img_path)

    def drop(self, event):
        file_path = event.data
        if file_path.startswith("{") and file_path.endswith("}"):
            file_path = file_path[1:-1]
        self.img_path = file_path
        print(f"File dropped: {file_path}")
        self.display_image(file_path)

    def display_image(self, file_path):
        try:
            img = Image.open(file_path)
            img = img.resize((245, 245))
            img = classification.create_rounded_image(img, 50)
            self.original_image = img.copy()
            img = ctk.CTkImage(light_image=img, dark_image=img, size=(250, 250))
            self.img_label.configure(image=img)
            self.result_img.configure(image=img)
            self.result_img.image = img
            self.img_label.image = img  # Keep a reference to avoid garbage collection
            self.upload_frame.place_forget()
            self.img_section_frame.place(relx=0.1, rely=0.35, anchor="nw")

        except Exception as e:
            print(f"Error displaying image: {e}")

    def classification(self):
        print("Classification button clicked")
        diseases = ["Normal", "Diabetic Retinopathy", "Glaucoma", "Cataract",
                    "Age related macula", "Hypertension", "Myopia"]

        if self.img_path != "":
            wait_label = ctk.CTkLabel(self.main_frame, text="wait...",
                                      font=("Arial", 16, "bold"), fg_color="skyblue", bg_color="#5597CD")
            wait_label.place(relx=0.5, rely=0.5, anchor="center", width=100)
            self.root.update()

            self.class_model = self.class_model_thread.join()
            print("class model loaded")
            img = classification.loadImg(self.img_path)
            img = classification.resizeImg(img)
            img, f = classification.crop(img)
            if f:
                img = classification.enhanceImg(img)
                pred = (self.class_model.predict(np.array([img/255.0])) >= 0.5).astype(int)
                result = ", ".join(map(str, ([diseases[i] for i in range(len(pred[0])) if pred[0][i] == 1])))
                if result == "":
                    result = "Other"
                self.disease = result
                self.result2_label.configure(text=result, text_color="red")

                wait_label.place_forget()
                self.main_frame.place_forget()
                self.classification_result_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

            else:
                messagebox.showerror("Error", "Bad Image, \nplease insert another image with good resolution..")

        else:
            messagebox.showerror("Error", "Please Upload Image first..")

    def optic_disk_segmentation(self):
        print("Optic Disk Segmentation button clicked")
        if self.img_path != "":
            wait_label = ctk.CTkLabel(self.main_frame, text="wait...",
                                      font=("Arial", 16, "bold"), fg_color="skyblue", bg_color="#5597CD")
            wait_label.place(relx=0.5, rely=0.5, anchor="center", width=100)
            self.root.update()

            self.optic_model = self.optic_model_thread.join()
            print("optic model loaded")
            img = segmentation.read_image(self.img_path)
            pred = np.where(self.optic_model.predict(np.array([img]))>=0.6, 255, 0).astype(np.uint8)
            print(pred)
            mask = np.where(np.array(pred[0][:,:,1])>=0.6, 255, 0)
            edgs = segmentation.find_contours(np.array(mask).astype(np.uint8))
            crooped_img = segmentation.crop_contours(img, edgs)
            cv.drawContours(img, edgs, -1, (0, 255, 0), 1)
            img = Image.fromarray(img)
            self.original_image = img.copy()
            crooped_img = Image.fromarray(crooped_img)
            self.masked_image = crooped_img.copy()
            self.masked_image = self.masked_image.resize((100, 150))
            im1 = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 250))
            self.im1_label.configure(image=im1)

            im2 = ctk.CTkImage(light_image=crooped_img, dark_image=crooped_img, size=(100, 150))
            self.im2_label.configure(image=im2)

            wait_label.place_forget()
            self.main_frame.place_forget()
            self.segmentation_result_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

        else:
            messagebox.showerror("Error", "Please Upload Image first..")

    def vessel_segmentation(self):
        print("Vessel Segmentation button clicked")
        if self.img_path != "":
            wait_label = ctk.CTkLabel(self.main_frame, text="wait...",
                                      font=("Arial", 16, "bold"), fg_color="skyblue", bg_color="#5597CD")
            wait_label.place(relx=0.5, rely=0.5, anchor="center", width=100)
            self.root.update()
            self.vessel_model = self.vessel_model_thread.join()
            print("vessel model loaded")
            img = segmentation.read_image_with_preprocess(self.img_path)
            img_no_process = Image.open(self.img_path)
            img_no_process = img_no_process.resize((512, 512))
            img_no_process = np.array(img_no_process)

            pred = np.where(self.vessel_model.predict(np.array([img])) >= 0.6, 255, 0).astype(np.uint8)
            print(pred)
            mask = pred[0]
            edgs = segmentation.find_contours(np.array(mask).astype(np.uint8))

            _, binary_mask = cv.threshold(mask, 1, 255, cv.THRESH_BINARY)
            binary_mask = Image.fromarray(binary_mask).convert('RGB')
            crooped_img = cv.bitwise_and(img_no_process, np.array(binary_mask))

            cv.drawContours(img_no_process, edgs, -1, (0, 255, 0), 1)

            img_no_process = Image.fromarray(img_no_process)
            crooped_img = Image.fromarray(crooped_img)

            self.original_image = img_no_process.copy()
            self.masked_image = crooped_img.copy()
            self.masked_image = self.masked_image.resize((300, 300))

            im1 = ctk.CTkImage(light_image=img_no_process, dark_image=img_no_process, size=(300, 300))
            self.im1_label.configure(image=im1)

            im2 = ctk.CTkImage(light_image=crooped_img, dark_image=crooped_img, size=(300, 300))
            self.im2_label.configure(image=im2)

            wait_label.place_forget()
            self.main_frame.place_forget()
            self.segmentation_result_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

        else:
            messagebox.showerror("Error", "Please Upload Image first..")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = EyeCareApp(root)
    root.mainloop()
