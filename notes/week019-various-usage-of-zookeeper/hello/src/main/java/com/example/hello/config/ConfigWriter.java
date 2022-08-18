package com.example.hello.config;

import org.apache.zookeeper.CreateMode;
import org.apache.zookeeper.KeeperException;
import org.apache.zookeeper.ZooDefs;
import org.apache.zookeeper.ZooKeeper;
import org.apache.zookeeper.data.Stat;

public class ConfigWriter {
	
	private ZooKeeper zookeeper;
    private String configPath;
    public ConfigWriter(ZooKeeper zookeeper, String configPath) {
        this.zookeeper = zookeeper;
        this.configPath = configPath;
    }

    public void writeConfig(String configData) throws KeeperException, InterruptedException {
        Stat stat = zookeeper.exists(configPath, false);
        if (stat == null) {
            zookeeper.create(configPath, configData.getBytes(), ZooDefs.Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);
        } else {
            zookeeper.setData(configPath, configData.getBytes(), -1);
        }
    }

    public static void main(String[] args) throws Exception {
        ZooKeeper zookeeper = new ZooKeeper("localhost:2181", 30000, null);
        ConfigWriter writer = new ConfigWriter(zookeeper, "/configuration");
        writer.writeConfig("Hello");
        zookeeper.close();
    }
}
