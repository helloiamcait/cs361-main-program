import ast
import time


def generate_email():
    with open('../pipes/email_content_generator.txt', 'r') as email_content_pipe:
        email_content_str = email_content_pipe.read()
    email_content_pipe.close()

    if email_content_str != '':
        email_content_list = ast.literal_eval(email_content_str)
        recipient_name = email_content_list[0]
        recipient_email = email_content_list[1]
        sender_name = email_content_list[2]
        sender_email = email_content_list[3]
        email_content = email_content_list[4]

        with open('../text/email_template.txt', 'r') as email_template:
            email_template_str = email_template.read()
        email_template.close()

        email_draft = email_template_str.format(recipient_name = recipient_name,
                                    recipient_email = recipient_email,
                                    sender_name = sender_name,
                                    sender_email = sender_email,
                                    email_content = email_content
                                    )
                
        with open('../pipes/email_content_generator.txt', 'w') as email_content_pipe:
            email_content_pipe.write(email_draft)
        email_content_pipe.close()

if __name__ == "__main__":
    while True:
        generate_email()
        time.sleep(2)