import requests
import facebook as fb


pageID = '147456461783047'
accessToken = 'EAAXPTAAjTwcBOZBhco2ZATa0NNxcQxVknaZCQTBFVEe41op29eyZCZA3I78tLuHkJOwMiOUwSKvTtjnN0rZArQRCceF9m1h1QkA98oo2JWVYifAzronPe36KZCMPWQzpXShCaButJOZAQYCMVmk9PaXzV63JJf6TtWFGCxsbxVEU3Gz6kMSBXRtpXvZAAuItr5sVCYPdILGoZD'
asafb = fb.GraphAPI(accessToken)

#input      : The username and the profile picture from his data
#description: This funtion creates a publication on the feed of eagle defender
#output     : void
def postTextToPage(user):
    user = "¡Felcidades "+ user + "! Por llegar al salón de la fama :D"
    url = f'https://graph.facebook.com/v18.0/{pageID}/feed?message={user}&access_token={accessToken}'
    try:
        r = requests.post(url)
        r.raise_for_status()
        return r.status_code
    except requests.exceptions.HTTPError as errh:
        print("Error HTTP:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error de conexión:", errc)
    except requests.exceptions.Timeout as errt:
        print("Error de tiempo de espera:", errt)
    except requests.exceptions.RequestException as err:
        print("Error de solicitud:", err)


#postTextToPage("UsuarioGenerico")


#input      : The username and the profile picture from his data
#description: This funtion creates a publication on the feed of eagle defender
#output     : void
def postImageToPage(user, profilePic):
    user = "¡Felcidades "+ user + "! Por llegar al salón de la fama :D"
    try:
        asafb.put_photo(open(profilePic, "rb"), message=user)
    except requests.exceptions.HTTPError as errh:
        print("Error HTTP:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error de conexión:", errc)
    except requests.exceptions.Timeout as errt:
        print("Error de tiempo de espera:", errt)
    except requests.exceptions.RequestException as err:
        print("Error de solicitud:", err)

#postImageToPage("Tzalil", "C:\\Users\\crseg\\OneDrive\\Escritorio\\Tzalil.png") Usage example