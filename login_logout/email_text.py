def registration_text(first_name, last_name, link):
    text = f"""
            Hello Greetings from ResumeMakers. :)

            Hey there {first_name} {last_name}

            We received a request that you need register to ResumeMaker

            Please use this hyperlink to set password to your account: 
            {link}

            If you did not initiate this request, you can safely ignore this email.

            Greetings,

            Team ResumeMaker
            """
    return text


def password_text(first_name, last_name, link):
    text = f"""
            Hello Greetings from ResumeMakers. :)
    
            Hey there {first_name} {last_name}
    
            We received a request that you forgot your password, don't worry, we got your back
    
            Please use this hyperlink to set password to your account: 
            {link}
    
            If you did not initiate this request, you can safely ignore this email.
    
            Greetings,
    
            Team ResumeMaker
            """
    return text
