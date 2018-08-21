# notifications

1. Install **wkhtmltopdf** to create pdfs for emails:
    ```bash
    # on mac
    brew install caskroom/cask/brew-cask
    brew cask install wkhtmltopdf
    ```

1. Use the following environment variables if outside of ec2 (note that the only available aws regions for sending emails are: **us-east-1**, **us-west-2**, **eu-west-1**):
    ```bash
    - AWS_ACCESS_KEY_ID=your_api_key
    - AWS_SECRET_ACCESS_KEY=your_secret_key
    - AWS_EMAIL_REGION=your_region
    ```

1. Run bash in image:
    ```bash
    docker run -it incs/notificationserver bash
    ```
