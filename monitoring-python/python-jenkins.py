import boto3

client = boto3.client('ecr')
def describe_java_gradle_repo():
  describe_repo = client.describe_images(
    repositoryName='java-gradle'
  )
  imageDetails = (describe_repo['imageDetails'])

  # Sort by date(newest first)
  sorted_images = sorted(imageDetails, key=lambda x: x['imagePushedAt'], reverse=True)

  for image in sorted_images:
    image_tag = (image['imageTags'])
    print(image_tag)
    return image_tag

describe_java_gradle_repo()