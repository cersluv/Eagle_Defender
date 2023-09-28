#include "registrationWindow.h"
RegistrationWindow::RegistrationWindow()
        : previewSquareX(550), previewSquareY(100), previewSquareSize(100), isRegistered(false), imageUploaded(false) {
    InitWindow(800, 600, "Registration Window");

    // Initialize registration form fields and rectangles
    // ...

    SetTargetFPS(60);
}

RegistrationWindow::~RegistrationWindow() {
    CloseWindow();
}

void RegistrationWindow::Run() {
    while (!WindowShouldClose()) {
        HandleInput();
        DrawUI();
    }
}

bool RegistrationWindow::IsPasswordValid(const char* password) {
    // You can implement password regulations here (e.g., length, special characters)
    return (strlen(password) >= 6);
}

void RegistrationWindow::HandleInput() {
    if (!isRegistered) {
        if (IsMouseButtonPressed(MOUSE_LEFT_BUTTON)) {
            // Check if the user clicks the Register button
            if (CheckCollisionPointRec(GetMousePosition(), registerButton)) {
                if (strcmp(password, confirmPassword) == 0) {
                    if (IsPasswordValid(password)) {
                        isRegistered = true;
                    } else {
                        // Password does not meet regulations, display an error message
                        MessageBox("Password is not valid!\nMinimum length: 6 characters", "Registration Error");
                    }
                } else {
                    // Passwords don't match, display an error message
                    MessageBox("Passwords do not match!", "Registration Error");
                }
            }
        }

        // Check for image upload
        if (IsFileDropped()) {
            int count;
            char** files = GetDroppedFiles(&count);
            if (count > 0) {
                UnloadTexture(uploadedImage); // Unload previous image, if any
                uploadedImage = LoadTexture(files[0]); // Load the new image
                ClearDroppedFiles(); // Clear dropped files list
                imageUploaded = true;
            }
        }
    }
}

void RegistrationWindow::DrawUI() {
    BeginDrawing();
    ClearBackground(RAYWHITE);

    // Draw registration form and image upload
    // ...

    EndDrawing();
}

int main() {
    RegistrationWindow registrationApp;
    registrationApp.Run();

    return 0;
}