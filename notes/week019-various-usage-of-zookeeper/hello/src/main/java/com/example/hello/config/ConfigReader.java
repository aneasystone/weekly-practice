package com.example.hello.config;

import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooKeeper;

public class ConfigReader implements Watcher {

    private ZooKeeper zookeeper;
    private String configPath;
    public ConfigReader(ZooKeeper zookeeper, String configPath) {
        this.zookeeper = zookeeper;
        this.configPath = configPath;
    }

    @Override
    public void process(WatchedEvent watchedEvent) {
        if (watchedEvent.getType() == Watcher.Event.EventType.NodeDataChanged) {
            readConfig();
        }
    }

    public void readConfig() {
        try {
            byte[] data = zookeeper.getData(configPath, this, null/*stat*/);
            System.out.println(new String(data));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
	
    public static void main(String[] args) throws Exception {
        ZooKeeper zookeeper = new ZooKeeper("localhost:2181", 30000, null);
        ConfigReader reader = new ConfigReader(zookeeper, "/configuration");
        reader.readConfig();
        Thread.sleep(Long.MAX_VALUE);
    }
}
