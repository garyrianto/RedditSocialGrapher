package gephifyer;
import java.awt.Color;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;

import org.gephi.data.attributes.api.AttributeColumn;
import org.gephi.data.attributes.api.AttributeController;
import org.gephi.data.attributes.api.AttributeModel;
import org.gephi.graph.api.DirectedGraph;
import org.gephi.graph.api.GraphController;
import org.gephi.graph.api.GraphModel;
import org.gephi.io.exporter.api.ExportController;
import org.gephi.io.importer.api.Container;
import org.gephi.io.importer.api.EdgeDefault;
import org.gephi.io.importer.api.ImportController;
import org.gephi.io.importer.spi.FileImporter;
import org.gephi.io.processor.plugin.DefaultProcessor;
import org.gephi.partition.api.Partition;
import org.gephi.partition.api.PartitionController;
import org.gephi.partition.plugin.NodeColorTransformer;
import org.gephi.preview.api.PreviewController;
import org.gephi.preview.api.PreviewModel;
import org.gephi.preview.api.PreviewProperty;
import org.gephi.preview.types.DependantOriginalColor;
import org.gephi.project.api.ProjectController;
import org.gephi.project.api.Workspace;
import org.gephi.ranking.api.Ranking;
import org.gephi.ranking.api.RankingController;
import org.gephi.ranking.plugin.transformer.AbstractSizeTransformer;
import org.gephi.statistics.plugin.Modularity;
import org.openide.util.Lookup;
import org.gephi.layout.plugin.openord.*;

public class Gephifyer {
	
	public void doStuff(String[] args)
	{
		String filename = new String();
		try{
			filename = args[0];
		} catch (ArrayIndexOutOfBoundsException ex) {
			System.out.println("Supply the subreddit name as the argument.");
			System.exit(0);
		}
		filename += ".csv";
		ProjectController pc = Lookup.getDefault().lookup(ProjectController.class);
		pc.newProject();
		Workspace workspace = pc.getCurrentWorkspace();
		
		ImportController importController = Lookup.getDefault().lookup(ImportController.class);
		Container container;
		try{
			File file = new File(filename);
			//File file = new File(getClass().getResource("askscience.csv").toURI());
			container = importController.importFile(file);
			container.getLoader().setEdgeDefault(EdgeDefault.DIRECTED);
			container.setAllowAutoNode(false); // don't create missing nodes
		} catch (Exception ex) {
			ex.printStackTrace();
			return;
		}
		
		// Append imported data to graph api
		importController.process(container, new DefaultProcessor(), workspace);
		
		GraphModel graphModel = Lookup.getDefault().lookup(GraphController.class).getModel();
		DirectedGraph directedGraph = graphModel.getDirectedGraph();
		// Now let's manipulate the graph api, which stores / serves graphs
		System.out.println("Nodes: " + directedGraph.getNodeCount() + "\nEdges: " + directedGraph.getEdgeCount());
		
		//Run OpenOrd.
		OpenOrdLayout layout = new OpenOrdLayout(null);
		layout.setGraphModel(graphModel);
		layout.resetPropertiesValues();
		layout.initAlgo();
		layout.goAlgo();
		while (layout.canAlgo()) // This is only possible because OpenOrd has a finite number of iterations.
		{
			layout.goAlgo();
		}
		
		AttributeModel attributemodel = Lookup.getDefault().lookup(AttributeController.class).getModel();
		
		// Get modularity for coloring
		Modularity modularity = new Modularity();
		modularity.setUseWeight(true);
		modularity.setRandom(true);
		modularity.setResolution(1.0);
		modularity.execute(graphModel, attributemodel);
		// Partition with modularity
		AttributeColumn modcol = attributemodel.getNodeTable().getColumn(Modularity.MODULARITY_CLASS);
		PartitionController partitionController = Lookup.getDefault().lookup(PartitionController.class);
		Partition p = partitionController.buildPartition(modcol, directedGraph);
		NodeColorTransformer nodeColorTransformer = new NodeColorTransformer();
        nodeColorTransformer.randomizeColors(p);
        partitionController.transform(p, nodeColorTransformer);
		
		// Ranking
		RankingController rankingController = Lookup.getDefault().lookup(RankingController.class);
        Ranking degreeRanking = rankingController.getModel().getRanking(Ranking.NODE_ELEMENT, Ranking.INDEGREE_RANKING);
        AbstractSizeTransformer sizeTransformer = (AbstractSizeTransformer) rankingController.getModel().getTransformer(Ranking.NODE_ELEMENT, org.gephi.ranking.api.Transformer.RENDERABLE_SIZE);
        sizeTransformer.setMinSize(5.0f);
        sizeTransformer.setMaxSize(40.0f);
        rankingController.transform(degreeRanking,sizeTransformer);
        
        // Finally the preview model
        PreviewController previewController = Lookup.getDefault().lookup(PreviewController.class);
        PreviewModel previewModel = previewController.getModel();
        previewModel.getProperties().putValue(PreviewProperty.SHOW_NODE_LABELS, Boolean.TRUE);
        previewModel.getProperties().putValue(PreviewProperty.NODE_LABEL_COLOR, new DependantOriginalColor(Color.BLACK));
        previewModel.getProperties().putValue(PreviewProperty.EDGE_CURVED, Boolean.FALSE);
        previewModel.getProperties().putValue(PreviewProperty.EDGE_OPACITY, 50);
        previewModel.getProperties().putValue(PreviewProperty.EDGE_RADIUS, 10f);
        previewModel.getProperties().putValue(PreviewProperty.BACKGROUND_COLOR, Color.TRANSLUCENT);
        previewController.refreshPreview();
        
        System.out.println("starting export");
        ExportController ec = Lookup.getDefault().lookup(ExportController.class);
        try{
        	ec.exportFile(new File("askscience.svg"));
        }
        catch (IOException ex){
        	ex.printStackTrace();
        	return;
        }
        System.out.println("Done.");
	}
	
	public static void main(String[] args)
	{
		Gephifyer g = new Gephifyer();
		g.doStuff(args);
	}
}
