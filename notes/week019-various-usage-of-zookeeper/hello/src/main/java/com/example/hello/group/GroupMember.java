package com.example.hello.group;

import java.util.List;
import java.util.Random;

import org.apache.zookeeper.CreateMode;
import org.apache.zookeeper.KeeperException;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooDefs;
import org.apache.zookeeper.ZooKeeper;
import org.apache.zookeeper.data.Stat;

public class GroupMember implements Watcher {
    
    private ZooKeeper zookeeper;
    private String groupPath;
    public GroupMember(ZooKeeper zookeeper, String groupPath) {
        this.zookeeper = zookeeper;
        this.groupPath = groupPath;
    }

    @Override
    public void process(WatchedEvent watchedEvent) {
        if (watchedEvent.getType() == Event.EventType.NodeChildrenChanged) {
            this.list();
        }
    }

    public void list() {
        try {
            List<String> members = zookeeper.getChildren(this.groupPath, this);
            System.out.println("Members: " + String.join(",", members));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void join(String memberName) {
        try {
			Stat stat = zookeeper.exists(this.groupPath, false);
			if (stat == null) {
				zookeeper.create(this.groupPath, null, ZooDefs.Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);
			}
			
            String path = zookeeper.create(
                    this.groupPath + "/" + memberName, null, ZooDefs.Ids.OPEN_ACL_UNSAFE, CreateMode.EPHEMERAL);
            System.out.println("Created: " + path);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) throws Exception {
        ZooKeeper zookeeper = new ZooKeeper("localhost:2181", 30000, null);
        GroupMember member = new GroupMember(zookeeper, "/groups");
        member.join("member-" + new Random().nextInt(1000));
        member.list();
        Thread.sleep(Long.MAX_VALUE);
    }
}
