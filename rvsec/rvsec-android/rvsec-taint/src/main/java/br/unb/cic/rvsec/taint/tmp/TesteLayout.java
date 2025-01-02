package br.unb.cic.rvsec.taint.tmp;

import java.io.File;
import java.io.IOException;
import java.util.HashSet;
import java.util.Set;

import org.xmlpull.v1.XmlPullParserException;

import br.unb.cic.rvsec.taint.model.ActivityInfo;
import br.unb.cic.rvsec.taint.model.ApkInfo;
import soot.Scene;
import soot.SootClass;
import soot.jimple.infoflow.android.axml.AXmlNode;
import soot.jimple.infoflow.android.manifest.ProcessManifest;
import soot.jimple.infoflow.android.manifest.binary.BinaryManifestActivity;
import soot.jimple.infoflow.android.resources.ARSCFileParser;
import soot.jimple.infoflow.util.SystemClassHandler;

public class TesteLayout {
	public static final String INTENT_FILTER = "intent-filter";
	public static final String ACTION = "action";
	public static final String MAIN = "android.intent.action.MAIN";

	public void execute(String apkPath) throws IOException, XmlPullParserException {
		ApkInfo apkInfo = new ApkInfo(apkPath);
		final File targetAPK = new File(apkPath);

		// Parse the resource file
		long beforeARSC = System.nanoTime();
		ARSCFileParser resources = new ARSCFileParser();
		resources.parse(targetAPK.getAbsolutePath());
		System.out.println("ARSC file parsing took " + (System.nanoTime() - beforeARSC) / 1E9 + " seconds");

		// To look for callbacks, we need to start somewhere. We use the Android
		// lifecycle methods for this purpose.
		try (ProcessManifest processManifest = new ProcessManifest(targetAPK, resources)) {
			AXmlNode manifest = processManifest.getManifest();

			String manifestPackage = manifest.getAttribute("package").getValue().toString();
			apkInfo.setManifestPackage(manifestPackage);
			boolean samePackage = false;

			for (BinaryManifestActivity binaryManifestActivity : processManifest.getActivities()) {
				ActivityInfo activityInfo = readActivity(binaryManifestActivity);
				System.out.println(activityInfo);
				if(!activityInfo.getPackageName().startsWith(apkInfo.getManifestPackage())) {
					samePackage = false;
				}
				apkInfo.addActivity(activityInfo);
			}

			apkInfo.setActivitiesAreInSamePackage(samePackage);

			SystemClassHandler.v().setExcludeSystemComponents(false);
			Set<String> entryPoints = processManifest.getEntryPointClasses();
			Set<SootClass> entrypoints = new HashSet<>(entryPoints.size());
			for (String className : entryPoints) {
				SootClass sc = Scene.v().getSootClassUnsafe(className);
				if (sc != null)
					entrypoints.add(sc);
			}
			for (SootClass sootClass : entrypoints) {
				System.out.println(sootClass);
			}
		}
	}



	private ActivityInfo readActivity(BinaryManifestActivity binaryManifestActivity) {
		AXmlNode act = binaryManifestActivity.getAXmlNode();
		String actName = act.getAttribute("name").getValue().toString();
		boolean isMain = false;
		for (AXmlNode child : act.getChildren()) {
			if (INTENT_FILTER.equals(child.getTag())) {
				for (AXmlNode grandchild : child.getChildren()) {
					if(ACTION.equals(grandchild.getTag())) {
						String actionName = grandchild.getAttribute("name").getValue().toString();
						if(MAIN.equals(actionName)) {
							isMain = true;
						}
					}
				}
			}
		}
		return new ActivityInfo(actName, isMain);
	}

	public static void main(String[] args) {
		String baseDir = "/pedro/desenvolvimento/workspaces/workspaces-doutorado/workspace-rv/rvsec/rv-android/apks_mini/";
		String apk = baseDir + "cryptoapp.apk";

		try {
			new TesteLayout().execute(apk);
		} catch (IOException | XmlPullParserException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
