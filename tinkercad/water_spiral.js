// Convenience Declarations For Dependencies.
// 'Core' Is Configured In Libraries Section.
// Some of these may not be used by this example.
var Conversions = Core.Conversions;
var Debug = Core.Debug;
var Path2D = Core.Path2D;
var Point2D = Core.Point2D;
var Point3D = Core.Point3D;
var Matrix2D = Core.Matrix2D;
var Matrix3D = Core.Matrix3D;
var Mesh3D = Core.Mesh3D;
var Plugin = Core.Plugin;
var Tess = Core.Tess;
var Sketch2D = Core.Sketch2D;
var Solid = Core.Solid;
var Vector2D = Core.Vector2D;
var Vector3D = Core.Vector3D;

// Template Code:
params = [
    { "id": "H"     , "displayName": "H"    , "type": "int", "rangeMin": 1, "rangeMax": 5, "default": 1 },
    { "id": "F"     , "displayName": "F"    , "type": "int", "rangeMin": 1, "rangeMax": 360, "default": 360 },
    { "id": "grow"  , "displayName": "grow" , "type": "float", "rangeMin": 0, "rangeMax": 1, "default": 0.02 },
    { "id": "border", "displayName": "border" , "type": "float", "rangeMin": 1, "rangeMax": 10, "default": 1 },
    { "id": "D"     , "displayName": "D"    , "type": "float", "rangeMin": 1, "rangeMax": 500, "default": 100 },
    { "id": "growB" , "displayName": "growB", "type": "float", "rangeMin": 0, "rangeMax": 1, "default": 0.02 }
];

function process(params) {
  Debug.log("Start processing ...");
  var H = params["H"];
  var F = params["F"]*H;
  var grow = params["grow"];
  var D = params["D"];
  var growB = params["growB"];
  var border = params["border"];
  
  var coords = [];
  for(var z=0;z<F;z++){
    var matRot = new Matrix3D();
    matRot.rotationX(z*Math.PI/180);
    var DN = D - growB*z;
    var y2 = Math.cos(z*Math.PI/180)*DN;
    var z2 = Math.sin(z*Math.PI/180)*DN;

    //#0
    var v = new Vector3D(-grow*z,-border,0);
    v.transform(matRot);
    coords.push(new Array(v.x,y2+v.y,z2+v.z));
    //#1
    v = new Vector3D(-grow*z,0,0);
    v.transform(matRot);
    coords.push(new Array(v.x,y2+v.y,z2+v.z));
    //#2
    v = new Vector3D(1+grow*z,0,0);
    v.transform(matRot);
    coords.push(new Array(v.x,y2+v.y,z2+v.z));
    //#3
    v = new Vector3D(1+grow*z,-border,0);
    v.transform(matRot);
    coords.push(new Array(v.x,y2+v.y,z2+v.z));

    //#4
    v = new Vector3D(-grow*z+0.2,-border,0);
    v.transform(matRot);
    coords.push(new Array(v.x,y2+v.y,z2+v.z));
    //#5
    v = new Vector3D(-grow*z+0.2,-0.2,0);
    v.transform(matRot);
    coords.push(new Array(v.x,y2+v.y,z2+v.z));
    //#6
    v = new Vector3D(0.8+grow*z,-0.2,0);
    v.transform(matRot);
    coords.push(new Array(v.x,y2+v.y,z2+v.z));
    //#7
    v = new Vector3D(0.8+grow*z,-border,0);
    v.transform(matRot);
    coords.push(new Array(v.x,y2+v.y,z2+v.z));
  }
  Debug.log("Coords length:" + coords.length);
  var GN=8;
  var mesh = new Mesh3D();

  var v0=0;
  var v1=1;
  var v2=2;
  var v3=3;
  var v4=4;
  var v5=5;
  var v6=6;
  var v7=7;
  
  var l=coords.length-1;
  var v8=l-7;
  var v9=l-6;
  var v10=l-5;
  var v11=l-4;
  var v12=l-3;
  var v13=l-2;
  var v14=l-1;
  var v15=l;
  
  /*Debug.log("0:"+v0);
  Debug.log("1:"+v1);
  Debug.log("2:"+v2);
  Debug.log("3:"+v3);
  Debug.log("4:"+v4);
  Debug.log("5:"+v5);
  Debug.log("6:"+v6);
  Debug.log("7:"+v7);
  Debug.log("8:"+v8);
  Debug.log("9:"+v9);
  Debug.log("10:"+v10);
  Debug.log("11:"+v11);
  Debug.log("12:"+v12);
  Debug.log("13:"+v13);
  Debug.log("14:"+v14);
  Debug.log("15:"+v15);

  
  Debug.log(coords[v0]);
  Debug.log(coords[v1]);
  Debug.log(coords[v2]);
  Debug.log(coords[v3]);
  Debug.log(coords[v4]);
  Debug.log(coords[v5]);
  Debug.log(coords[v6]);
  Debug.log(coords[v7]);

  Debug.log(coords[v8]);
  Debug.log(coords[v9]);
  Debug.log(coords[v10]);
  Debug.log(coords[v11]);
  Debug.log(coords[v12]);
  Debug.log(coords[v13]);
  Debug.log(coords[v14]);
  Debug.log(coords[v15]);*/
  
  mesh.quad(coords[v0],coords[v1],coords[v5],coords[v4]);
  mesh.quad(coords[v1],coords[v2],coords[v6],coords[v5]);
  mesh.quad(coords[v6],coords[v2],coords[v3],coords[v7]);
  
  mesh.quad(coords[v9],coords[v8],coords[v13],coords[v12]);
  mesh.quad(coords[v10],coords[v9],coords[v14],coords[v13]);
  mesh.quad(coords[v14],coords[v10],coords[v11],coords[v15]);
  Debug.log((F-2)*GN+7);
  for(var x = 0;x<F-1;x++){
          var k=x+1;
          v0=x*GN;
          v1=x*GN+1;
          v2=x*GN+2;
          v3=x*GN+3;
          v4=x*GN+4;
          v5=x*GN+5;
          v6=x*GN+6;
          v7=x*GN+7;
      
          v8=k*GN;
          v9=k*GN+1;
          v10=k*GN+2;
          v11=k*GN+3;
          v12=k*GN+4;
          v13=k*GN+5;
          v14=k*GN+6;
          v15=k*GN+7;
      
          mesh.quad(coords[v0],coords[v4],coords[v12],coords[v8]);
          mesh.quad(coords[v5],coords[v13],coords[v12],coords[v4]);
          mesh.quad(coords[v5],coords[v13],coords[v14],coords[v6]);
          mesh.quad(coords[v6],coords[v14],coords[v15],coords[v7]);

            //#mesh.quad(coords[v6],coords[v2],coords[v10],coords[v14]);

          mesh.quad(coords[v7],coords[v15],coords[v11],coords[v3]);
          mesh.quad(coords[v3],coords[v11],coords[v10],coords[v2]);
          mesh.quad(coords[v1],coords[v2],coords[v10],coords[v9]);
          mesh.quad(coords[v1],coords[v9],coords[v8],coords[v0]);
    
            //#mesh.quad(coords[v9],coords[v12],coords[v1],coords[v5]);
  }
  
  // Center mesh
  var bbox = [0,0,0, 0,0,0];
  for (var i2 = 0; i2 < coords.length; i2++) {
    var vc = coords[i2];
    if (i2 === 0) {
      bbox[0] = bbox[3] = vc[0];
      bbox[1] = bbox[4] = vc[1];
      bbox[2] = bbox[5] = vc[2];
    } else {
      bbox[0] = Math.min(bbox[0], vc[0]);
      bbox[1] = Math.min(bbox[1], vc[1]);
      bbox[2] = Math.min(bbox[2], vc[2]);
      bbox[3] = Math.max(bbox[3], vc[0]);
      bbox[4] = Math.max(bbox[4], vc[1]);
      bbox[5] = Math.max(bbox[5], vc[2]);
    }
  }
  var cx = (bbox[3] + bbox[0]) / 2;
  var cy = (bbox[4] + bbox[1]) / 2;
  var xoff = -cx;
  var yoff = -cy;
  var zoff = -bbox[2];
  mesh.transform([1,0,0,0, 0,1,0,0, 0,0,1,0, xoff,yoff,zoff,1]);
  
  var solid = Solid.make(mesh);
  Debug.log("... end processing."); 
  return solid;
}