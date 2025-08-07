import ast

def generate_email():
    with open('../pipes/email_content_generator.txt', 'r') as email_content_pipe:
        email_content_str = email_content_pipe.read()
    email_content_pipe.close()

    email_content_list = ast.literal_eval(email_content_str)
    recipient_name = email_content_list[0]
    recipient_email = email_content_list[1]
    sender_name = email_content_list[2]
    sender_email = email_content_list[3]
    email_content = email_content_list[4]

    with open('../text/email_template.txt', 'r') as email_template:
        email_template_str = email_template.read()
    email_template.close()

    print(f'{email_template_str}')

generate_email()