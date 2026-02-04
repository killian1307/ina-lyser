from assets.package.website import WebsiteBuilder
import assets.package.detector as detector

# Just building the website
detector.load_model()
website=WebsiteBuilder()
website.create_page()