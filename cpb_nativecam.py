abc = hou.selectedNodes()
ds = []
dp = []
nos = []
for i in abc:
	if i.type().category().name() == "Object" :
		nos.append(i)

print("selected objects: " + str(nos))
c = 0
while len(nos) > c :
	for i in nos :
		subs = i.children()
		for s in subs :
			print("checking sub-node type : " + s.type().name())
			if s.type().name() == "cam" :
				if (s in ds) != True :
					ds.append(s)
					dp.append(s.path())
			if s.type().category().name() == "Object" :
				nos.append(s)
		c = c + 1

if len(ds) > 0 :
	c = 0
	obj = hou.node('/obj')
	ch = 0
	try:
		ch = hou.node('/obj/cam_convert')
		print("chopnet found, using it : " + ch.path())
		xu = ch.children()
		for u in xu: u.destroy()
	except:
		print("chopnet not found, creating it...")
		ch = obj.createNode("chopnet", "cam_convert")
	oo = ch.createNode("ropnet", "save_animation")
	print("ropnet: " + oo.path())
	
	for i in ds :
		print("\tharvested camera: " + i.name())
		print("\t" + dp[c] + "\n")
		cc = 0
		try: 
			cc = hou.node('obj/native_cam_' + str(c))
			print("\tnative camera found, using it : " + cc.path())
		except:
			print("\tnative camera not found, creating it...")
			cc = obj.createNode("cam", ("native_cam_" + str(c)))
		print("\t\tnative cam : " + cc.path())
		fe = ch.createNode("fetch", ("fetch_cam_parms_" + str(c)))
		fe.parm('nodepath').set(i.path())
		fe.parm('path').set('aperture focal')
		ge = ch.createNode("object", ("get_cam_xf_" + str(c)))
		ge.parm('targetpath').set(i.path())
		ge.parm('compute').set(8)
		mg = ch.createNode("merge", ("merge_channels_" + str(c)))
		mg.setNextInput(ge)
		mg.setNextInput(fe)
		sm = ch.createNode("null", "LIVE_" + str(c))
		sm.setInput(0,mg)
		fi = ch.createNode("file", ("load_saved" + str(c)))
		fi.parm('file').set('$HIP/clip/native_cam_' + str(c) + '.bclip')
		sw = ch.createNode("switch", ("switch_to_saved" + str(c)))
		sw.setNextInput(sm)
		sw.setNextInput(fi)
		ou = ch.createNode("export", "OUT_" + str(c))
		ou.setInput(0,sw)
		ou.parm('nodepath').set(cc.path())
		ou.parm('path').set('tx ty tz rx ry rz sx sy sz aperture focal')
		ou.setCurrent(True)
		ou.setSelected(True)
		ou.setDisplayFlag(True)
		ou.setExportFlag(True)
		bc = oo.createNode("channel", ("save_bclip_" + str(c)))
		bc.parm('choppath').set(sm.path())
		bc.parm('chopoutput').set('$HIP/clip/native_cam_' + str(c) + '.bclip')
	ch.layoutChildren()
