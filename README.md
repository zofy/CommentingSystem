# CommentingSystem
Simple commenting system which sorts comment by popularity

# Download

git clone https://github.com/zofy/CommentingSystem.git projectname && cd projectname

# Run
After cloning this project just run the following command:
python manage.py runserver

Five comments are displayed per page, you can change that in views.py

Moreover, comments are sorted according to their popularity via Lower bound of Wilson score confidence interval for Bernoulli parameter

For generating new comments just open comment_generator.py set number of comments to generate(NUMBER_OF_COMMENTS) and run:
python comment_generator.py
