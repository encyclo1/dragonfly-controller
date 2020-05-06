package edu.unm.dragonfly;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;


public class DisplaySceneSample extends Application {

    private static DashboardController controller;

    @Override
    public void start(Stage stage) throws Exception {

        FXMLLoader loader = new FXMLLoader(getClass().getResource("/dashboard.fxml"));

        Parent root = loader.load();
        controller = loader.getController();

        Scene scene = new Scene(root);

        // set title, size, and add JavaFX scene to stage
        stage.setTitle("Dragonfly Dashboard");
        stage.setWidth(800);
        stage.setHeight(700);
        stage.setScene(scene);
        stage.show();
    }

    /**
     * Stops and releases all resources used in application.
     */
    @Override
    public void stop() {

        controller.terminate();
    }

    /**
     * Opens and runs application.
     *
     * @param args arguments passed to this application
     */
    public static void main(String[] args) {

        Application.launch(args);
    }

}