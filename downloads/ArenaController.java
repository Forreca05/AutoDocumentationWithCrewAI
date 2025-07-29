package com.t10g06.baba.controller.game;

import com.t10g06.baba.Game;
import com.t10g06.baba.controller.game.gameevents.GameEvent;
import com.t10g06.baba.controller.game.gameevents.QuitEvent;
import com.t10g06.baba.controller.game.gameevents.RestartEvent;
import com.t10g06.baba.controller.game.gameevents.WinEvent;
import com.t10g06.baba.controller.game.observers.GameObserver;
import com.t10g06.baba.controller.game.observers.QuitObserver;
import com.t10g06.baba.controller.game.observers.RestartObserver;
import com.t10g06.baba.controller.game.observers.WinConditionObserver;
import com.t10g06.baba.controller.game.ruleparsing.WordController;
import com.t10g06.baba.gui.GUI;
import com.t10g06.baba.model.game.arena.Arena;
import com.t10g06.baba.model.game.arena.LoaderArenaBuilder;
import com.t10g06.baba.model.game.elements.Element;
import com.t10g06.baba.model.levels.Levels;
import com.t10g06.baba.states.GameState;
import com.t10g06.baba.states.LevelsState;

import java.awt.*;
import java.io.IOException;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.List;

import static com.t10g06.baba.Sound.playSound;

public class ArenaController extends GameController {
    private final List<GameController> controllers;
    private final List<GameObserver> observers;

    public ArenaController(Arena arena) {
        super(arena);
        this.controllers = new ArrayList<>();
        this.observers = new ArrayList<>();

        controllers.add(new YouController(arena));
        controllers.add(new WordController(arena));
        controllers.add(new SinkController(arena));
        controllers.add(new HotMeltController(arena));
        controllers.add(new OpenShutController(arena));
        controllers.add(new DefeatController(arena));

        observers.add(new WinConditionObserver());
        observers.add(new RestartObserver());
        observers.add(new QuitObserver());

    }

    public void addObserver(GameObserver observer) {
        observers.add(observer);
    }

    public void removeObserver(GameObserver observer) {
        observers.remove(observer);
    }

    private void notifyObservers(GameEvent event, Game game) {
        for (GameObserver observer : observers) {
            observer.onGameEvent(event, game);
        }
    }


    @Override
    public void step(Game game, GUI.ACTION action, long time) throws IOException, URISyntaxException, FontFormatException {
        switch (action) {
            case QUIT -> notifyObservers(new QuitEvent(), game);
            case RESTART -> notifyObservers(new RestartEvent(), game);
            default -> {
                for (GameController controller : controllers) {
                    controller.step(game, action, time);
                }
                checkWinCondition(game);
            }
        }
    }

    private void checkWinCondition(Game game) {
        for (Element youElement : getModel().getYouElements()) {
            for (Element winElement : getModel().getWinElements()) {
                if (youElement.getPosition().equals(winElement.getPosition())) {
                    notifyObservers(new WinEvent(), game);
                    return;
                }
            }
        }
    }
}