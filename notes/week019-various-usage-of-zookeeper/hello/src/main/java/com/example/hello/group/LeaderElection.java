package com.example.hello.group;

import java.util.Comparator;
import java.util.List;

import org.apache.zookeeper.CreateMode;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooDefs;
import org.apache.zookeeper.ZooKeeper;

public class LeaderElection implements Watcher {

    private ZooKeeper zookeeper;
    private String groupPath;
    private String currentNode;
    
	public LeaderElection(ZooKeeper zookeeper, String groupPath) {
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
            members.sort(Comparator.naturalOrder());
            if (this.currentNode.equals(this.groupPath + "/" + members.get(0))) {
                System.out.println("I'm the master");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void join(String memberName) {
        try {
            this.currentNode = zookeeper.create(
                    this.groupPath + "/" + memberName, null, ZooDefs.Ids.OPEN_ACL_UNSAFE, CreateMode.EPHEMERAL_SEQUENTIAL);
            System.out.println("Created: " + this.currentNode);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
	
    public static void main(String[] args) throws Exception {
        ZooKeeper zookeeper = new ZooKeeper("localhost:2181", 30000, null);
        LeaderElection member = new LeaderElection(zookeeper, "/groups");
        member.join("member-");
        member.list();
        Thread.sleep(Long.MAX_VALUE);
    }
}
