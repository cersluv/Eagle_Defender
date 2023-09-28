#ifndef EAGLE_DEFENDER_REGISTRATIONWINDOW_H
#define EAGLE_DEFENDER_REGISTRATIONWINDOW_H

#include "raylib.h"

class RegistrationWindow {
public:
    RegistrationWindow();
    ~RegistrationWindow();

    void Run();

private:
    bool IsPasswordValid(const char* password);

    void HandleInput();
    void DrawUI();

    // Registration form fields
    char username[256];
    char password[256];
    char confirmPassword[256];
    char favoriteSong[256];

    Rectangle usernameField;
    Rectangle passwordField;
    Rectangle confirmPasswordField;
    Rectangle favoriteSongField;
    Rectangle registerButton;

    const int previewSquareX;
    const int previewSquareY;
    const int previewSquareSize;
    Rectangle previewSquare;
    Texture2D uploadedImage;

    bool isRegistered;
    bool imageUploaded;
};

#endif //EAGLE_DEFENDER_REGISTRATIONWINDOW_H
